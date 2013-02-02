from django.conf.urls.defaults import *
from dbe.blog.models import *
from dbe.blog.views import PostView, Main, ArchiveMonth

urlpatterns = patterns("dbe.blog.views",
   (r"^post/(?P<dpk>\d+)/$"          , PostView.as_view(), {}, "post"),
   (r"^archive_month/(\d+)/(\d+)/$"  , ArchiveMonth.as_view(), {}, "archive_month"),
   (r"^$"                            , Main.as_view(), {}, "main"),
   # (r"^delete_comment/(\d+)/$"       , "delete_comment", {}, "delete_comment"),
)
