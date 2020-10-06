from django.contrib import admin
from .models import Post  #actually is posts.models but since both admin and models are in the same module posts, we do a relative import  

# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated", "timestamp"]   #all modeladmin methods,  displays mentioned
	list_display_links = ["updated"]                  #makes mentioned a link
	list_filter = ["updated", "timestamp"]              #lets filter by mentioned
	list_editable = ["title"]
	search_fields = ["title", "content"]                #lets search by mentione
	
	class Meta:                      #model referrenced is Post
		model = Post

admin.site.register(Post,PostModelAdmin) #default admin function that registers the model to admin site
