from django.contrib import admin

from .models import *

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
# Register your models here.
