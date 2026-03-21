from django.shortcuts import redirect, render
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .forms import CategoryForm, BlogForm
from django.template.defaultfilters import slugify


def _generate_unique_slug(title, exclude_id=None):
    base_slug = slugify(title) or 'post'
    slug = base_slug
    counter = 2

    while Blog.objects.exclude(pk=exclude_id).filter(slug=slug).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1

    return slug


# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.count()
    blogs_count = Blog.objects.count()
    context = {
        'category_count': category_count,
        'blogs_count': blogs_count
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='login')
def categories(request):
    context = {
        'categories': Category.objects.order_by('category_name'),
    }
    return render(request, 'dashboard/categories.html', context)


@login_required(login_url='login')
@require_POST
def delete_category(request, pk=None, category_id=None):
    resolved_id = pk if pk is not None else category_id
    category = get_object_or_404(Category, pk=resolved_id)
    category.delete()
    return redirect('categories')

@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()

    context = {
        'form': form
    }
    return render(request, 'dashboard/add_categories.html', context)

@login_required(login_url='login')
def edit_category(request, pk=None, category_id=None):
    resolved_id = pk if pk is not None else category_id
    category = get_object_or_404(Category, pk=resolved_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
        'pk': category.id,
    }
    return render(request, 'dashboard/edit_category.html', context)


@login_required(login_url='login')
def posts(request):
    context = {
        'posts': Blog.objects.order_by('-created_at'),
    }
    return render(request, 'dashboard/posts.html', context)


@login_required(login_url='login')
def add_post(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = _generate_unique_slug(post.title)
            post.save()
            return redirect('posts')
    else:
        form = BlogForm()

    context = {
        'form': form
    }
    return render(request, 'dashboard/add_post.html', context)


@login_required(login_url='login')
def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = _generate_unique_slug(post.title, exclude_id=post.id)
            post.save()
            return redirect('posts')
    else:
        form = BlogForm(instance=post)

    context = {
        'form': form,
        'pk': post.id,
    }
    return render(request, 'dashboard/edit_post.html', context)


@login_required(login_url='login')
@require_POST
def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('posts')
