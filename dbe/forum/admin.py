from django.contrib import admin
from dbe.forum.models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user"]

class ForumAdmin(admin.ModelAdmin):
    pass

class ThreadAdmin(admin.ModelAdmin):
    list_display = "title forum creator created".split()
    list_filter  = "forum creator".split()

class PostAdmin(admin.ModelAdmin):
    search_fields = "title creator".split()
    list_display  = "title thread creator created".split()


def create_user_profile(sender, **kwargs):
    """When creating a new user, make a profile for him."""
    user = kwargs["instance"]
    if not UserProfile.objects.filter(user=user):
        UserProfile(user=user).save()

post_save.connect(create_user_profile, sender=User)

admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserProfile, ProfileAdmin)
