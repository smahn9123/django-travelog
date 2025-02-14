from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Post
from .serializers import PostListSerializer


class PostListView(ListAPIView):
    queryset = Post.objects.all().defer("content").select_related("author")
    serializer_class = PostListSerializer


post_list = PostListView.as_view()
