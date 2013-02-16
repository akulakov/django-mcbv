from django.contrib import admin
from dbe.portfolio.models import *

class GroupAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title", "image_links"]

class ImageAdmin(admin.ModelAdmin):
    list_display = "__unicode__ title group created".split()
    list_filter  = ["group"]

admin.site.register(Group, GroupAdmin)
admin.site.register(Image, ImageAdmin)
