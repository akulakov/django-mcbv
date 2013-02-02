from django.contrib import admin
from dbe.blog.models import *


class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    display_fields = "title created".split()

class CommentAdmin(admin.ModelAdmin):
    display_fields = "post author created".split()

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
