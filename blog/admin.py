from django.contrib import admin

#1.importing the model
from .models import Post,Comment


# Register your models here.
#2.assigning decorting
'''The @admin.register()decorator performs	the	same function as the admin.site.register() function
	we have	replaced,	registering	the	ModelAdmin	class	that	it	decorates.'''

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

	#3.this will display in the list form
    list_display = ('title', 'slug', 'author', 'publish',   
                       'status')
	#4.You can see that	the	fields	displayed on the post list page	are	the ones you specified in the list_display attribute.The list page now includes	a right	sidebar	that allows	you	to	filter	the	results	by	the fields included in	the	list_filter	attribute
    list_filter = ('status', 'created', 'publish', 'author')
	
	#5.	A Search bar has appeared on the page.This is because we have defined a	list of	searchable fields using	the	search_fields attribute
    search_fields = ('title', 'body')
	
	#6.We have told	Django to prepopulate the slug field with the input	of	the	title field	using the prepopulated_fields attribute. 
    prepopulated_fields = {'slug': ('title',)}
	
	#7.Also, now, the author field is displayed	with a lookup widget that can scale	much better than a drop-down select	input when you have thousands of user
    raw_id_fields = ('author',)
	
	#8.Just	below the Search bar,there are navigation links	to	navigate through a date hierarchy:this has been	defined	by the date_hierarchy attribute
    date_hierarchy = 'publish'
	
	#9.You can also see that the posts are ordered by Status and Publish columns by	default.We have	specified the default order	using the ordering attribute.
    ordering = ('status', 'publish')
	
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin): 
    list_display = ('name', 'email', 'post', 'created', 'active') 
    list_filter = ('active', 'created', 'updated') 
    search_fields = ('name', 'email', 'body') 
    