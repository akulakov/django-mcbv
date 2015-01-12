from django import forms as f
from questionnaire.models import *

null_choice = [("---", "---")]

class SectionForm(f.Form):
    def __init__(self, *args, **kwargs):
        """ Add a field for every question.
            Field may be CharField or ChoiceField; field name is question.order.
        """
        section = kwargs.pop("section")
        super(SectionForm, self).__init__(*args, **kwargs)

        for question in section.questions.all():
            choices = question.choices
            kw      = dict(help_text=question.question)

            if choices:
                fld           = f.ChoiceField
                choices       = [c.strip() for c in choices.split(',')]
                kw["choices"] = [(c,c) for c in choices]
            else:
                fld              = f.CharField
                kw["max_length"] = 200

            self.fields[str(question.order)] = fld(**kw)
