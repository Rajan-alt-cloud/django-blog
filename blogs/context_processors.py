from .models import Category

def get_categories(request):
    categories = Category.objects.all()
    return {'category': categories}