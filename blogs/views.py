from multiprocessing import context

from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from .models import Blog, Category
from assignments.models import SocialLink

def home(request):
    category = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True, status=1).order_by("-created_at")
    featured_post = featured_posts.first()
    posts = Blog.objects.filter(is_featured=False, status=1).order_by("-created_at")
    context = {
        "category": category,
        "featured_post": featured_post,
        "featured_posts": featured_posts,
        "posts": posts,
        "SocialLink": SocialLink.objects.all(),
    }
    return render(request, 'home.html', context)

def categories_list(request):
    # Display all categories
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'category': categories,
        'SocialLink': SocialLink.objects.all(),
    }
    return render(request, 'categories_list.html', context)

def category_blogs(request, category_id):
    # Fetch the posts that belong to the category id
    posts = Blog.objects.filter(category_id=category_id, status=1)
    current_category = Category.objects.filter(id=category_id).first()
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'current_category': current_category,
        'category': categories,
        'SocialLink': SocialLink.objects.all(),
    }
    return render(request, 'category_blogs.html', context)
# Create your views here.

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status=1)
    context = {
        'single_blog': single_blog,
        'category': Category.objects.all(),
        'SocialLink': SocialLink.objects.all(),
    }
    return render(request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keyword', '').strip()
    posts = []
    if keyword:
        posts = Blog.objects.filter(
            Q(title__icontains=keyword,status=1) | 
            Q(short_description__icontains=keyword,status=1) | 
            Q(blog_body__icontains=keyword,status=1),
            status=1
        ).order_by("-created_at")
    
    context = {
        'keyword': keyword,
        'posts': posts,
        'category': Category.objects.all(),
        'SocialLink': SocialLink.objects.all(),
        'search_results': True,
    }
    return render(request, 'search_results.html', context)


def register(request):
    return render(request, 'register.html',context)