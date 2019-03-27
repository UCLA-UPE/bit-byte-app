from django.contrib import admin
from .models import Profile, Choice, SiteSettings

# Register your models here.
admin.site.register(Profile)
admin.site.register(Choice)
admin.site.register(SiteSettings)