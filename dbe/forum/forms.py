from django.forms import ModelForm
from forum.models import *
from shared.utils import ContainerFormMixin

class ProfileForm(ModelForm):
    class Meta:
        model   = UserProfile
        exclude = ["posts", "user"]

class PostForm(ContainerFormMixin, ModelForm):
    class Meta:
        model   = ForumPost
        exclude = ["creator", "thread"]
