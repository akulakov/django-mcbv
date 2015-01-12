from django.conf.urls import *
from django.contrib.auth.decorators import login_required as LR
from forum.models import *
from forum.views import *

urlpatterns = patterns("forum.views",
    (r"^forum/(?P<dpk>\d+)/$"             , ForumView.as_view(), {}, "forum"),
    (r"^thread/(?P<dpk>\d+)/$"            , ThreadView.as_view(), {}, "thread"),

    (r"^new_topic/(?P<dpk>\d+)/$"          , LR(NewTopic.as_view()), {}, "new_topic"),
    (r"^reply/(?P<dpk>\d+)/$"              , LR(Reply.as_view()), {}, "reply"),
    (r"^profile/(?P<mfpk>\d+)/$"           , LR(EditProfile.as_view()), {}, "profile"),

    (r""                                   , Main.as_view(), {}, "forum_main"),
)
