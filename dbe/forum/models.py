from django.db.models import *
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save

from dbe.settings import MEDIA_URL
from dbe.shared.utils import *


class Forum(BaseModel):
    title = CharField(max_length=60)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse2("forum", dpk=self.pk)

    def num_posts(self):
        return sum([t.num_posts() for t in self.threads.all()])

    def last_post(self):
        """Go over the list of threads and find the most recent post."""
        threads = self.threads.all()
        last    = None
        for thread in threads:
            lastp = thread.last_post()
            if lastp and (not last or lastp.created > last.created):
                last = lastp
        return last


class Thread(BaseModel):
    title   = CharField(max_length=60)
    created = DateTimeField(auto_now_add=True)
    creator = ForeignKey(User, blank=True, null=True)
    forum   = ForeignKey(Forum, related_name="threads")

    class Meta:
        ordering = ["-created"]

    def __unicode__(self):
        return unicode("%s - %s" % (self.creator, self.title))

    def get_absolute_url(self) : return reverse2("thread", dpk=self.pk)
    def last_post(self)        : return first(self.posts.all())
    def num_posts(self)        : return self.posts.count()
    def num_replies(self)      : return self.posts.count() - 1


class Post(BaseModel):
    title   = CharField(max_length=60)
    created = DateTimeField(auto_now_add=True)
    creator = ForeignKey(User, blank=True, null=True)
    thread  = ForeignKey(Thread, related_name="posts")
    body    = TextField(max_length=10000)

    class Meta:
        ordering = ["created"]

    def __unicode__(self):
        return u"%s - %s - %s" % (self.creator, self.thread, self.title)

    def short(self):
        created = self.created.strftime("%b %d, %I:%M %p")
        return u"%s - %s\n%s" % (self.creator, self.title, created)

    def profile_data(self):
        p = self.creator.profile
        return p.posts, p.avatar


class UserProfile(BaseModel):
    avatar = ImageField("Profile Pic", upload_to="images/", blank=True, null=True)
    posts  = IntegerField(default=0)
    user   = OneToOneField(User, related_name="profile")

    def __unicode__(self):
        return unicode(self.user)

    def increment_posts(self):
        self.posts += 1
        self.save()

    def avatar_image(self):
        return (MEDIA_URL + self.avatar.name) if self.avatar else None
