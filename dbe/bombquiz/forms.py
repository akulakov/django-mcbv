from django import forms as f
from django.forms.widgets import RadioSelect
from bombquiz.models import *

null_choice = [("---", "---")]
choices = [(c,c) for c in "yes no pass".split()]


class NewPlayerForm(f.ModelForm):
    class Meta:
        model   = PlayerRecord
        exclude = ["passed"]

class QuestionForm(f.Form):
    def __init__(self, *args, **kwargs):
        """Add the field for `question`."""
        question = kwargs.pop("question").question
        super(QuestionForm, self).__init__(*args, **kwargs)
        field = f.ChoiceField(choices=choices, widget=RadioSelect, help_text=question)
        self.fields["answer"] = field
