from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment

# Create your models here.

def upload_location(instance, filename):                                  #stores image file inside post folder in media_cdm
    return "%s/%s" %(instance.id, filename)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
        null=True, 
        blank=True, 
        width_field="width_field", 
        height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0) 
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)  #auto_now sets each time Post object is updated
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True) #auto_now_add sets first time Post object is created
 
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #return reverse("posts:detail", kwargs={"slug": self.slug})
        return reverse("detail", kwargs={"slug": self.slug})

    class Meta:
    	ordering=["-timestamp","-updated"] #orders posts based on latest timestamp, if same latest updated comes first
    
    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
    

def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)   #turns title into slug
    if new_slug is not None: #slug made
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()   #checks if slug already exists
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id) #appending id to the slug    
        return create_slug(instance, new_slug=new_slug) #recursive call again for new slug
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)


