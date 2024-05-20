from django.urls import path
from .views import BlogListView, BlogDetailView , BlogAllPostsView, BlogUserPostsView

urlpatterns = [
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/all/', BlogAllPostsView.as_view(), name='blog-all-posts'),
    path('blog/user/', BlogUserPostsView.as_view(), name='blog-user-posts'),
]
