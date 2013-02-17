from django.contrib import admin
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from dbe.questionnaire.models import *

class SectionInline(admin.TabularInline):
    model = Section
    extra = 6

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 4


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ["name", "section_links"]
    inlines = [SectionInline]

class UserQuestionnaireAdmin(admin.ModelAdmin):
    list_display = ["user", "questionnaire"]

class QuestionAdmin(admin.ModelAdmin):
    list_display = "question choices answer_type section".split()

class AnswerAdmin(admin.ModelAdmin):
    list_display = "answer question user_questionnaire".split()
    list_filter = "user_questionnaire answer".split()


class SectionAdmin(admin.ModelAdmin):
    list_display = "name questionnaire order".split()
    inlines = [QuestionInline]

    def response_change(self, request, obj):
        """ Determines the HttpResponse for the change_view stage.

            copied from admin.options.ModelAdmin
        """
        opts = obj._meta

        # Handle proxy models automatically created by .only() or .defer()
        verbose_name = opts.verbose_name
        if obj._deferred:
            opts_ = opts.proxy_for_model._meta
            verbose_name = opts_.verbose_name

        pk_value = obj._get_pk_val()

        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {'name': force_unicode(verbose_name), 'obj': force_unicode(obj)}
        if "_continue" in request.POST:
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            if "_popup" in request.REQUEST:
                return HttpResponseRedirect(request.path + "?_popup=1")
            else:
                return HttpResponseRedirect(request.path)
        elif "_saveasnew" in request.POST:
            msg = _('The %(name)s "%(obj)s" was added successfully. You may edit it again below.') % {'name': force_unicode(verbose_name), 'obj': obj}
            self.message_user(request, msg)
            return HttpResponseRedirect("../%s/" % pk_value)
        elif "_addanother" in request.POST:
            self.message_user(request, msg + ' ' + (_("You may add another %s below.") % force_unicode(verbose_name)))
            return HttpResponseRedirect("../add/")
        else:
            self.message_user(request, msg)
            return HttpResponseRedirect(reverse("admin:questionnaire_questionnaire_changelist"))


admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(UserQuestionnaire, UserQuestionnaireAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
