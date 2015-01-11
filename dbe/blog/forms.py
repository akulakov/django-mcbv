from django.forms import *
from blog.models import *

class CommentForm(ModelForm):
    class Meta:
        model = BlogComment
        exclude = ["post"]

    def clean_author(self):
        return self.cleaned_data.get("author") or "Anonymous"
