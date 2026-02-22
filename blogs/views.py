from django.shortcuts import redirect, render
from .models import Blog, Category

def home(request):
    category = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured=True, status='published').order_by("created_at")
    posts = Blog.objects.filter(is_featured=False, status='published').order_by("-created_at")
    context = {
        "category": category,
        "featured_posts": featured_posts,
        "posts": posts,
    }
    return render(request, 'home.html', context)

def categories_list(request):
    # Display all categories
    categories = Category.objects.all()
    context = {
        'categories': categories,
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
    }
    return render(request, 'category_blogs.html', context)
# Create your views here.
