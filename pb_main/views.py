from django.shortcuts import redirect, render
from django.templatetags.static import static

from blogs.models import Category, Blog
from assignments.models import About, SocialLink
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm    
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    categories = Category.objects.all()
    featured_posts = (
        Blog.objects.filter(status=1, is_featured=True)
        .select_related("category", "author")
        .order_by("-created_at")
    )
    featured_ids = list(featured_posts.values_list("id", flat=True))
    featured_post = featured_posts.first()
    hero_image_url = static("images/wrestlemania-vegas.jpg")
    if featured_post and featured_post.featured_image:
        image_field = featured_post.featured_image
        if image_field.storage.exists(image_field.name):
            hero_image_url = image_field.url
    posts = (
        Blog.objects.filter(status=1)
        .select_related("category", "author")
        .order_by("-created_at")
    )
    if featured_ids:
        posts = posts.exclude(pk__in=featured_ids)
    
    # Fetch about us - show only the latest one
    about = About.objects.order_by('-updated_at').first()
    
    # Fetch all social links
    social_links = SocialLink.objects.all()
    
    context = {
        "category": categories,
        "featured_post": featured_post,
        "featured_posts": featured_posts,
        "hero_image_url": hero_image_url,
        "posts": posts,
        "about": about,
        "SocialLink": social_links,
    }
    return render(request, "home.html", context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')  # Redirect to the same page or any other page after successful registration
        else:
            print(form.errors)  # Print form errors to the console for debugging
    else:
        form = RegistrationForm()
    context ={
        'form': form,
    }
    return render(request, 'register.html',context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in.')
                return redirect('home')

            messages.error(request, 'Invalid username or password.')

    context = {
        'form': form,
    }   

    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'You are now logged out.')
    return redirect('home')
