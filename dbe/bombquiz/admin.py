from django.contrib import admin
from dbe.bombquiz.models import *

class QuestionAdmin(admin.ModelAdmin):
    list_display = "question answer order".split()

class PlayerRecordAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "passed"]

class AnswerAdmin(admin.ModelAdmin):
    list_display = "answer player_record question correct".split()


admin.site.register(Question, QuestionAdmin)
admin.site.register(PlayerRecord, PlayerRecordAdmin)
admin.site.register(Answer, AnswerAdmin)
