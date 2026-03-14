from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class About(models.Model):
    about_heading = models.CharField(max_length=30)
    about_description = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "About"

    def clean(self):
        # Ensure only one About entry exists
        if About.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Only one About Us page is allowed. Please edit the existing one.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.about_heading


class SocialLink(models.Model):
    platform = models.CharField(max_length=30)
    url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Social Links"

    def __str__(self):
        return self.platform