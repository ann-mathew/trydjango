from rest_framework.generics import ListAPIView

from posts.models import Post

class PostListAPIView(ListAPIView):    #class based views
	queryset = Post.objects.all()
