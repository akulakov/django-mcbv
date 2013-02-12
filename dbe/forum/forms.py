from django.forms import ModelForm
from dbe.forum.models import *
from dbe.shared.utils import ContainerFormMixin

class ProfileForm(ModelForm):
    class Meta:
        model   = UserProfile
        exclude = ["posts", "user"]

class PostForm(ContainerFormMixin, ModelForm):
    class Meta:
        model   = Post
        exclude = ["creator", "thread"]
