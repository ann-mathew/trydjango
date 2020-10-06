from django.contrib import admin
from django.urls import path                   



from .views import PostListAPIView


urlpatterns = [
    path('', PostListAPIView.as_view() , name='list'),                    
    

    """path('create/', views.post_create),                         
    path('<slug:slug>/', views.post_detail, name='detail'),            
    path('<slug:slug>/edit/', views.post_update, name='update'),       
    path('<slug:slug>/delete/', views.post_delete),  """
]
