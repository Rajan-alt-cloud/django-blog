from django.contrib import admin

from .models import Category, Blog, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "created_at", "updated_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "blog", "content", "created_at", "updated_at")
    list_filter = ("blog", "created_at")
    search_fields = ("content",)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "created_at", "is_featured", "updated_at")
    list_filter = ("status", "category", "is_featured")
    search_fields = ("title", "short_description", "blog_body")
    list_editable = ("status", "is_featured")
    prepopulated_fields = {"slug": ("title",)}
