from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Blog
from django.shortcuts import get_object_or_404
import json
import jwt
from django.utils.decorators import method_decorator
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError

def token_required(f):
    def wrap(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)
        
        try:
            token = auth_header.split(" ")[1] 
            payload = jwt.decode(token, 'secret', algorithms=['HS384'])
            request.user_id = payload['id']
        except (IndexError, ExpiredSignatureError, InvalidTokenError):
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        return f(request, *args, **kwargs)
    
    return wrap

class BlogAllPostsView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        blogs = Blog.objects.filter(is_deleted=False)
        blog_data = [{'id': blog.id, 'title': blog.title, 
                      'description': blog.description,
                      'published_date': blog.published_date,
                      'author': blog.author.email} for blog in blogs]
        return JsonResponse(blog_data, safe=False)

class BlogUserPostsView(View):

    @method_decorator(csrf_exempt)
    @method_decorator(token_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        author_id = request.user_id
        blogs = Blog.objects.filter(is_deleted=False, author_id=author_id)
        blog_data = [{'id': blog.id, 'title': blog.title, 
                      'description': blog.description,
                      'published_date': blog.published_date,
                      'author': blog.author.email} for blog in blogs]
        return JsonResponse(blog_data, safe=False)

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
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS384'])
            author_id = payload['id']
            author = get_object_or_404(CustomUser, id=author_id)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'error': 'Error decoding token'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

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
    @method_decorator(token_required)
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