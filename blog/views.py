from django.shortcuts import render,get_object_or_404
#1.Paginatior module
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
#2.Import Post
from .models import Post,Comment

#Importing List View
from django.views.generic import ListView

#Importing the email form from the form.py
from .forms import EmailPostForm,CommentForm

#importing gmail to send the msg
from django.core.mail import send_mail

#importing taggit application
from taggit.models import Tag



# Create your views here.
def post_list(request,tag_slug=None):
    object_list= Post.published.all()

    #we create the tag 
    tag=None

    #writing the if condition for tag

    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        object_list=object_list.filter(tags__in=[tag])
	
    '''We instantiate the Paginator class with the number of objects 
	we want to display on each page'''
    paginator = Paginator(object_list, 3) # 3 posts in each page
	
    """We get the page	GET	parameter that indicates the current
	page number."""
    page = request.GET.get('page')
	
    try:
	    #We obtain the objects for the desired page calling the page() method of Paginator.
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})
    
                 
def post_detail(request,year,month,day,post):
    posts = get_object_or_404(Post,slug=post,status='published'
						,publish__year=year,publish__month=month,
							 publish__day=day)
    
    comments=posts.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment =comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = posts
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    # List of similar posts
    post_tags_ids = posts.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                 .exclude(id=posts.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:4]


    return render(request,'blog/post/detail.html',{'posts': posts,'comments':comments,'new_comment':new_comment,
                                    'comment_form':comment_form,'similar_posts':similar_posts})
				  
		

		
				  
class PostListView(ListView):
    #Use a specific QuerySet instead of retrieving	all	objects.Instead	of defining	a queryset attribute,we	could have specified model=Post and Django would have built the generic Post.objects.all() QuerySet for us.
    queryset = Post.published.all()
	#Use the context variable posts	for	the	query results.The default variable is object_list if we	don't specify any context_object_name.
    context_object_name = 'posts'
	#Paginate the result displaying	three objects per age.
    paginate_by = 3
	#Use a custom template to render the page.If we don't set a default	template,ListView will use blog/post_list.html.
    template_name = 'blog/post/list.html'
	
"""In order to keep pagination working,we have to use the right page object that is passed
	tothe	template.	Django's	ListView	generic	view passes	the	selected	page	in	a	
	variable	called	page_obj,	so	you	have	to edit	your	post/list.html	template	
	accordingly	to	include	the	paginator using	the	right	variable,	as	follows:
	{%	include	"pagination.html"	with	page=page_obj	%}"""

#post share by email function
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post,id=post_id, status='published')
    sent = False 
 
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                                          post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com',
 [cd['to']])
            sent = True
    else:
	    #When the view is loaded initially with	a GET request,we create	a	
		#new form instance that	will be	used to	display	the empty form in the template
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
	                                               'form':form,
												   'sent':sent})
           
