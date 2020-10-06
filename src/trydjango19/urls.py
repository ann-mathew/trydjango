"""trydjango19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include                        #include allows the other url file to be included
from django.conf import settings
from django.conf.urls.static import static

#import posts.views
from posts import views


urlpatterns = [
    path('admin/', admin.site.urls),                         #mapped to admin
    #path('posts/', include(("posts.urls","posts"),namespace='posts')),                   #mapped to the view post_detail
    path('', views.post_list, name='list'),                    
    path('create/', views.post_create),                         
    path('<slug:slug>/', views.post_detail, name='detail'),            
    path('<slug:slug>/edit/', views.post_update, name='update'),       
    path('<slug:slug>/delete/', views.post_delete),  
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

