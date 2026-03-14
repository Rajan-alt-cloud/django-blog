from django.contrib import admin
from .models import About, SocialLink

# Register your models here.
class AboutAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow adding if no About entry exists
        count = About.objects.all().count()
        if count == 0:
            return True
        return False

class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'updated_at']
    search_fields = ['platform']

admin.site.register(About, AboutAdmin)
admin.site.register(SocialLink, SocialLinkAdmin)

admin.site.site_header = "PB Admin"