from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Category"

    def __str__(self):
        return self.category_name


STATUS_CHOICES = ((0, "Draft"), (1, "Published"))


class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to="uploads/%Y/%m/%d/")
    short_description = models.TextField(max_length=500)
    blog_body = models.TextField(max_length=1000)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        base_slug = slugify(self.slug or self.title) or 'post'
        slug = base_slug
        counter = 2

        while Blog.objects.exclude(pk=self.pk).filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1

        self.slug = slug
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
    