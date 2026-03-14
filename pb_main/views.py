from django.shortcuts import render
from django.templatetags.static import static

from blogs.models import Category, Blog
from assignments.models import About, SocialLink


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
