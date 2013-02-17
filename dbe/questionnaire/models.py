from string import join
from django.db.models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from dbe.shared.utils import *

link = "<a href='%s'>%s</a>"


class Questionnaire(BaseModel):
    name = CharField(max_length=60, unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self, section=1):
        return reverse2("questionnaire", self.pk, section)

    def section_links(self):
        section_url = "admin:questionnaire_section_change"
        lst         = [(c.pk, c.name) for c in self.sections.all()]
        lst         = [ (reverse2(section_url, pk), name) for pk, name in lst ]
        return ", ".join( [link % c for c in lst] )
    section_links.allow_tags = True


class UserQuestionnaire(BaseModel):
    user          = ForeignKey(User, related_name="questionnaires", blank=True, null=True)
    questionnaire = ForeignKey(Questionnaire, related_name="user_questionnaires", blank=True, null=True)
    created       = DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.questionnaire)

    class Meta:
        ordering = ["user", "created"]


class Section(BaseModel):
    """Container for a few questions, shown on a single page."""
    name          = CharField(max_length=60, blank=True, null=True)
    questionnaire = ForeignKey(Questionnaire, related_name="sections", blank=True, null=True)
    order         = IntegerField()

    class Meta:
        ordering        = ["order"]
        unique_together = [["questionnaire", "order"]]

    def __unicode__(self):
        return "[%s] (%s) %s" % (self.questionnaire, self.order, self.name or '')

    def title(self):
        return "(%s) %s" % (self.order, self.name or '')



class Question(BaseModel):
    question    = CharField(max_length=200)
    choices     = CharField(max_length=500, blank=True, null=True)
    answer_type = CharField(max_length=6, choices=(("str", "str"), ("int", "int")))
    section     = ForeignKey(Section, related_name="questions", blank=True, null=True)
    order       = IntegerField()

    class Meta:
        ordering        = ["order"]
        unique_together = [["section", "order"]]

    def __unicode__(self):
        return "%s: %s" % (self.section, self.question)


class Answer(BaseModel):
    answer             = CharField(max_length=200)
    question           = ForeignKey(Question, related_name="answers", blank=True, null=True)
    user_questionnaire = ForeignKey(UserQuestionnaire, related_name="answers", blank=True, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.user_questionnaire, self.answer)

    class Meta:
        ordering = ["question__section__order", "question__order"]
