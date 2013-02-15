from markdown import markdown

from django.template import loader
from django.db.models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from settings import MEDIA_URL
from dbe.shared.utils import *

btn_tpl  = "<div class='%s' id='%s_%s'><img class='btn' src='%simg/admin/icon-%s.gif' /></div>"
namelink = "<a href='%s'>%s</a> <a style='float:right; font-size:0.6em;' href='%s'>edit</a>"
dellink  = "<a href='%s'>Delete</a>"


class Project(BaseModel):
    creator = ForeignKey(User, related_name="projects", blank=True, null=True)
    project = CharField(max_length=60)

    def __unicode__(self):
        return self.project

class Tag(BaseModel):
    creator = ForeignKey(User, related_name="tags", blank=True, null=True)
    tag     = CharField(max_length=30)

    def __unicode__(self):
        return self.tag


class Issue(BaseModel):
    name       = CharField(max_length=60)
    creator    = ForeignKey(User, related_name="created_issues", blank=True, null=True)
    body       = TextField(max_length=3000, default='', blank=True)
    body_html  = TextField(blank=True, null=True)

    owner      = ForeignKey(User, related_name="issues", blank=True, null=True)
    priority   = IntegerField(default=0, blank=True, null=True)
    difficulty = IntegerField(default=0, blank=True, null=True)
    progress   = IntegerField(default=0)

    closed     = BooleanField(default=False)
    created    = DateTimeField(auto_now_add=True)
    project    = ForeignKey(Project, related_name="issues", blank=True, null=True)
    tags       = ManyToManyField(Tag, related_name="issues", blank=True, null=True)

    def get_absolute_url(self):
        return reverse2("issue", dpk=self.pk)

    def save(self):
        self.body_html = markdown(self.body)
        super(Issue, self).save()

    def name_(self):
        link    = reverse2("issue", dpk=self.pk)
        editlnk = reverse2("update_issue_detail", mfpk=self.pk)
        return namelink % (link, self.name, editlnk)
    name_.allow_tags = True

    def progress_(self):
        return loader.render_to_string("progress.html", dict(pk=self.pk))
    progress_.allow_tags = True
    progress_.admin_order_field = "progress"

    def closed_(self):
        onoff = "on" if self.closed else "off"
        return btn_tpl % ("toggle closed", 'd', self.pk, MEDIA_URL, onoff)
    closed_.allow_tags = True
    closed_.admin_order_field = "closed"

    def created_(self):
        return self.created.strftime("%b %d %Y")
    created_.admin_order_field = "created"

    def owner_(self):
        return self.owner or ''
    owner_.admin_order_field = "owner"

    def project_(self):
        return self.project or ''
    project_.admin_order_field = "project"

    def delete_(self):
        return dellink % reverse2("update_issue", self.pk, "delete")
    delete_.allow_tags = True


class Comment(BaseModel):
    creator   = ForeignKey(User, related_name="comments", blank=True, null=True)
    issue     = ForeignKey(Issue, related_name="comments", blank=True, null=True)
    created   = DateTimeField(auto_now_add=True)
    body      = TextField(max_length=3000)
    body_html = TextField()

    def save(self):
        self.body_html = markdown(self.body)
        super(Comment, self).save()

    def __unicode__(self):
        return unicode(self.issue.name if self.issue else '') + " : " + self.body[:20]
