from django.contrib import admin
from dbe.issues.models import *

class ProjectAdmin(admin.ModelAdmin):
    list_display = ["project"]

class TagsAdmin(admin.ModelAdmin):
    list_display = ["tag"]

class CommentAdmin(admin.ModelAdmin):
    pass
    # list_display = ["tag"]

class IssueAdmin(admin.ModelAdmin):
    list_display   = "name_ owner_ priority difficulty project_ created_ progress_ closed_ delete_".split()
    list_filter    = "priority difficulty project tags closed owner".split()
    date_hierarchy = "created"
    # search_fields = ["name", "tags"]

admin.site.register(Comment, CommentAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag, TagsAdmin)
