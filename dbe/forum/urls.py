from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required as LR
from dbe.forum.models import *
from dbe.forum.views import *

urlpatterns = patterns("dbe.forum.views",
    (r"^forum/(?P<dpk>\d+)/$"             , ForumView.as_view(), {}, "forum"),
    (r"^thread/(?P<dpk>\d+)/$"            , ThreadView.as_view(), {}, "thread"),

    (r"^new_topic/(?P<dpk>\d+)/$"          , LR(NewTopic.as_view()), {}, "new_topic"),
    (r"^reply/(?P<dpk>\d+)/$"              , LR(Reply.as_view()), {}, "reply"),
    (r"^profile/(?P<mfpk>\d+)/$"           , LR(EditProfile.as_view()), {}, "profile"),

    (r""                                   , Main.as_view(), {}, "forum_main"),
)
