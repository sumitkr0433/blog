from django.db import models

#1.importing user
from django.contrib.auth.models import User

#2.Importing time
from django.utils import timezone

#9.importing the url
from django.urls import reverse
#inserting the taggit manager
from taggit.managers import TaggableManager


#6.Writing the models
class PublishedManager(models.Manager): 
    def get_queryset(self): 
        return super(PublishedManager, self).get_queryset().filter(status='published')

#3Create your models here.
class Post(models.Model): 
    STATUS_CHOICES = ( 
        ('draft', 'Draft'), 
        ('published', 'Published'), 
    ) 
    title = models.CharField(max_length=250) 
    slug = models.SlugField(max_length=250,  
                            unique_for_date='publish') 
    author = models.ForeignKey(User, 
                               on_delete=models.CASCADE,
                               related_name='blog_posts') 
    body = models.TextField() 
    publish = models.DateTimeField(default=timezone.now)
    #4.this filed get value automatic	value so it is not visible in the admin panel
    created = models.DateTimeField(auto_now_add=True) 
	#4.this filed get value automatic	value so it is not visible in the admin panel
    updated = models.DateTimeField(auto_now=True) 
    status = models.CharField(max_length=10,  
                              choices=STATUS_CHOICES, 
                              default='draft')
		
		
	#7creating the model manager for the objects						  
    objects = models.Manager() # The default manager.
	#8.Creating the object for the customised  model
    published = PublishedManager() # Our custom manager.
	
	#creating the object for taggable
    tags = TaggableManager()
							  
	#4.meta class for ordering in admin panel						  
    class Meta:
        ordering=('-publish',)
	#5.Writing the string represtation of object in admin panel	
    def __str__(self):
        return self.title
		
	#10.defining  get absolute urls
    '''The convention in Django is to add a get_absolute_url() method to the model that returns the canonical URL of	
	the	object.	For	this method,we will use the reverse() method that allows you to	build URLs by their	name and	
	passing	optional parameters'''	
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
							 
class Comment(models.Model): 
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80) 
    email = models.EmailField() 
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 
 
    class Meta: 
        ordering = ('created',) 
 
    def __str__(self): 
        return 'Comment by {} on {}'.format(self.name, self.post)