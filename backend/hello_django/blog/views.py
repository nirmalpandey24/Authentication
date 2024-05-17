from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Blog
from django.shortcuts import get_object_or_404
import json

class BlogListView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        blogs = Blog.objects.filter(is_deleted=False)
        blog_data = [{'id': blog.id, 'title': blog.title, 
                      'description': blog.description,
                      'published_date': blog.published_date,
                      'author': blog.author.email} for blog in blogs]
        return JsonResponse(blog_data, safe=False)

    def post(self, request):
        blog_data = json.loads(request.body)
        author_id = blog_data.get('author')
        author = get_object_or_404(CustomUser, id=author_id)

        try:
            blog = Blog.objects.create(title=blog_data['title'],
                                       description=blog_data['description'],
                                       author=author)
            return JsonResponse({'id': blog.id, 'title': blog.title,
                                 'description': blog.description,
                                 'published_date': blog.published_date,
                                 'author': author.email}, status=201)
        except KeyError:
            return JsonResponse({'error': 'Invalid data provided'}, status=400)


class BlogDetailView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        blog_data = {'id': blog.id, 'title': blog.title,
                     'description': blog.description,
                     'published_date': blog.published_date,
                     'author': blog.author.email}
        return JsonResponse(blog_data)

    def put(self, request, pk):
        blog_data = json.loads(request.body)
        try:
            blog = get_object_or_404(Blog, id=pk)
            blog.title = blog_data['title']
            blog.description = blog_data['description']
            blog.save()
            return JsonResponse({'id': blog.id, 'title': blog.title,
                                 'description': blog.description,
                                 'published_date': blog.published_date,
                                 'author': blog.author.email})
        except KeyError:
            return JsonResponse({'error': 'Invalid data provided'}, status=400)

    def patch(self, request, pk):
        blog_data = json.loads(request.body)
        try:
            blog = get_object_or_404(Blog, id=pk)
            if 'title' in blog_data:
                blog.title = blog_data['title']
            if 'description' in blog_data:
                blog.description = blog_data['description']
            if 'published_date' in blog_data:
                blog.published_date = blog_data['published_date']
            if 'author' in blog_data:
                blog.author = blog_data['author']
            blog.save()
            return JsonResponse({'id': blog.id, 'title': blog.title,
                                 'description': blog.description,
                                 'published_date': blog.published_date,
                                 'author': blog.author.email})
        except KeyError:
            return JsonResponse({'error': 'Invalid data provided'}, status=400)

    def delete(self, request, pk):
        try:
            blog = get_object_or_404(Blog, id=pk)
            blog.delete()
            return JsonResponse({'message': 'Blog deleted'}, status=204)
        except Blog.DoesNotExist:
            return JsonResponse({'error': 'Blog not found'}, status=404)
