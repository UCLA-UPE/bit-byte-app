from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SiteSettings)
admin.site.register(Profile)
admin.site.register(Choice)
admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(EventCheckoff)
admin.site.register(Team)
