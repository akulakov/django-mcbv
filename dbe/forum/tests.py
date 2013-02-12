from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from dbe.forum.models import *

class SimpleTest(TestCase):
    def setUp(self):
        forum  = Forum.objects.create(title="forum")
        user   = User.objects.create_user("ak", "ak@abc.org", "pwd")
        thread = Thread.objects.create(title="thread", creator=user, forum=forum)

        UserProfile.objects.create(user=user)
        Site.objects.create(domain="test.org", name="test.org")
        Post.objects.create(title="post", body="body", creator=user, thread=thread)

    def content_test(self, url, values):
        """Get content of url and test that each of items in `values` list is present."""
        r = self.c.get(url)
        self.assertEquals(r.status_code, 200)
        for v in values:
            self.assertTrue(v in r.content)

    def test(self):
        self.c = Client()
        self.c.login(username="ak", password="pwd")

        # test forum listing, thread listing and post page
        self.content_test("/forum/", ['<a href="/forum/forum/1/">forum</a>'])
        self.content_test("/forum/forum/1/", ['<a href="/forum/thread/1/">thread</a>', "ak - post"])

        self.content_test("/forum/thread/1/",
              ['<div class="ttitle">thread</div>',
               '<span class="title">post</span>',
               'body <br />', 'by ak |'])

        # test creation of a new thread and a reply
        r = self.c.post("/forum/new_topic/1/", {"title": "thread2", "body": "body2"})
        r = self.c.post("/forum/reply/2/", {"title": "post2", "body": "body3"})

        self.content_test("/forum/thread/2/",
                ['<div class="ttitle">thread2</div>',
                 '<span class="title">post2</span>',
                 'body2 <br />', 'body3 <br />'])
