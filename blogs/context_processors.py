from .models import Category
from assignments.models import SocialLink

def get_categories(request):
    categories = Category.objects.all()
    return {'category': categories}

def get_SocialLink(request):
    social_links = SocialLink.objects.all()
    return {'SocialLink': social_links}