from django.shortcuts import redirect, render
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .forms import CategoryForm, BlogForm, UserForm, AddUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


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


@login_required(login_url='login')
@permission_required('auth.view_user', raise_exception=True)
def users(request):
    users = User.objects.all()
    context = {
        'users': users
    }   
    return render(request, 'dashboard/users.html', context)


@login_required(login_url='login')
def user_profile(request):
    context = {
        'user_obj': request.user,
    }
    return render(request, 'dashboard/user_profile.html', context)


@login_required(login_url='login')
@permission_required('auth.change_user', raise_exception=True)
def edit_user(request, pk):
    user_obj = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserForm(instance=user_obj)

    context = {
        'form': form,
        'pk': user_obj.id,
    }
    return render(request, 'dashboard/edit_user.html', context)


@login_required(login_url='login')
@permission_required('auth.add_user', raise_exception=True)
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user_obj = form.save()
            messages.success(request, f'User "{user_obj.username}" has been created successfully.')
            return redirect('users')
        messages.error(request, 'User could not be created. Please fix the form errors and submit again.')
    else:
        form = AddUserForm()

    context = {
        'form': form,
    }
    return render(request, 'dashboard/add_user.html', context)


@login_required(login_url='login')
@permission_required('auth.delete_user', raise_exception=True)
@require_POST
def delete_user(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    user_obj.delete()
    return redirect('users')

