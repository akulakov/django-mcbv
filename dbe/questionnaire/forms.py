from django import forms as f
from dbe.questionnaire.models import *

null_choice = [("---", "---")]

class SectionForm(f.Form):
    def __init__(self, *args, **kwargs):
        """ Add a field for every question.

            Field may be CharField or ChoiceField; field name is question.order.

            Note: `self.order` keeps a list of field names in right order; probably not really
            necessary since fields are already created in right order and simple iteration in
            template should always (?) work right.  (removed `self.order` for now)
        """
        section = kwargs.pop("section")
        super(SectionForm, self).__init__(*args, **kwargs)

        for question in section.questions.all():
            choices = question.choices
            fld     = f.CharField
            kw      = dict(help_text=question.question)

            if choices:
                choices       = [c.strip() for c in choices.split(',')]
                choices       = null_choice + [(c,c) for c in choices]
                fld           = f.ChoiceField
                kw["choices"] = choices
            else:
                kw["max_length"] = 200

            self.fields[str(question.order)] = fld(**kw)
