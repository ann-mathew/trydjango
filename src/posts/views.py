from urllib.parse import quote_plus #converts strings to share string
from django.http import HttpResponse, HttpResponseRedirect, Http404 #for user permissions
from django.shortcuts import render, get_object_or_404, redirect #render looks for an object related to a call
from django.contrib import messages
from django.core.mail import mail_admins
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

# Create your views here.

from .models import Post                          
from .forms import PostForm                   

def post_list(request):                                    
    queryset_list = Post.objects.filter(draft=False)        #.filter(publish__lte=timezone.now())  wont contain posts with publish date in future    
                                                            #.all() query_set now contains all posts
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
            ).distinct() 

    paginator = Paginator(queryset_list, 5)                #Paginator paginates queryset_list in pages of 10, paginator contains paginated pages
    page_request_var= "page"                                #changing values of "page" gets automatically reflected in url
    page_number = request.GET.get(page_request_var)         #.get() retrieves a page and assigns the page a number, stored in page_number
    try:
        queryset = paginator.page(page_number)  #paginator.page() method returns an object of given page number from the paginated results
                                                   
    except PageNotAnInteger:
        queryset = paginator.page(1)                        #if page parameter in the query string is not available, return the first page
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)      #if the value of the page parameter exceeds num_pages then return the last page
    context={
        "object_list": queryset,                            #queryset, which is the object (of Page type) of a page, is assigned to object_list
        "title": "List",
        "page_request_var": page_request_var
    }
    return render(request, "post_list.html", context)       #context is rendered 
    

def post_create(request):                                    #view to handle requests (by sending response )
    if not request.user.is_staff or not request.user.is_superuser:  #user permissions
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None) #form set to PostForm, arguments check validation of form, if invalid asks to fill
    if form.is_valid():
        instance = form.save(commit=False)                
        instance.user = request.user
        instance.save()                                      #saves form data to db, imples it's valid
        messages.success(request, "successfully created!")
        return HttpResponseRedirect(instance.get_absolute_url()) #redirects to /posts/<id> after saving, comes from model.py
    context = {                                              #context sent to post_form.html
        "form": form
    }
    return render(request,"post_form.html", context)
        

def post_detail(request,slug):                                 #to list details of each posts on clicking title, url path updated since takes arguments
    instance = get_object_or_404(Post, slug=slug)                 #instance set to one matching specific id by querying
    share_string = quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
    }
    return render(request,"post_detail.html", context)       #context sent to post_detail.html
    #return HttpResponse(<h1>Detail</h1>)


def post_update(request, slug):                           #url path updated in url.py as it takes id argument
    instance = get_object_or_404(Post, slug=slug)                 #form updated for specific id    
    form = PostForm(request.POST or None, request.FILES or None, instance=instance) #instance=instance show existing form data in form                
    if form.is_valid():
        instance = form.save(commit=False)                
        instance.save()                                      #saves form data to db, imples it's valid
        messages.success(request, "updated!")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }
    return render(request,"post_form.html", context)


def post_delete(request, slug):                                 
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "succesfully deleted!")
    return redirect("list")                             #deletes and redirects to /posts





 