from django.urls import path
from . import views

urlpatterns = [
    path('', views.categories_list, name='categories_list'),
    path('<int:category_id>/', views.category_blogs, name='category_blogs'),
]