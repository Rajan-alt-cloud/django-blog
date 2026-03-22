from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Categories crud
    path('categories/', views.categories, name='categories'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('categories/add/', views.add_category, name='add_category'),

    # Blogs crud
    path('posts/', views.posts, name='posts'),
    path('posts/edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('posts/delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('posts/add/', views.add_post, name='add_post'),
    # User profile
    path('users/', views.users, name='users'),
    path('user/', views.user_profile, name='user_profile'),
    path('users/edit/<int:pk>/', views.edit_user, name='edit_user'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/delete/<int:pk>/', views.delete_user, name='delete_user'),
]