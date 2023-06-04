from django.contrib import admin
from .models import Section, Discussion, Reply

# Register your models here.
admin.site.register(Section)
admin.site.register(Discussion)
admin.site.register(Reply)