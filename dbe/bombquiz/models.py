from django.db.models import *
from dbe.shared.utils import *


class Question(BaseModel):
    question = CharField(max_length=200, unique=True)
    answer   = CharField(max_length=60)
    order    = IntegerField(unique=True)

    def __unicode__(self):
        return "%d. %s - %s" % (self.order, self.question, self.answer)

    class Meta:
        ordering = ["order"]


class PlayerRecord(BaseModel):
    name    = CharField(max_length=60)
    email   = EmailField(max_length=120)
    created = DateTimeField(auto_now_add=True)
    passed  = BooleanField(default=False)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.email)

    class Meta:
        ordering        = ["created"]
        unique_together = [["name", "email"]]


class Answer(BaseModel):
    answer        = CharField(max_length=60)
    player_record = ForeignKey(PlayerRecord, related_name="answers")
    question      = ForeignKey(Question, related_name="answers")
    correct       = BooleanField()

    def __unicode__(self):
        return "%s, %s" % (self.answer, self.correct)

    class Meta:
        ordering        = ["question__order"]
        unique_together = [["question", "player_record"]]
