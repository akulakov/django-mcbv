from django.conf.urls.defaults import *
from dbe.issues.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("dbe.issues.views",
    (r"^delete-comment/(\d+)/$", "delete_comment", {}, "delete_comment"),

    (r"^update-issue/(\d+)/(delete)/$", "update_issue", {}, "update_issue"),

    (r"^update-issue/(\d+)/(closed|progress)/(on|off|\d+)/$", "update_issue", {}, "update_issue"),


    (r"^update-issue-detail/(?P<mfpk>\d+)/$", UpdateIssue.as_view(), {}, "update_issue_detail"),

    (r"^issue/(?P<dpk>\d+)/$", ViewIssue.as_view(), {}, "issue"),

    (r"^update-comment/(?P<mfpk>\d+)/$", UpdateComment.as_view(), {}, "update_comment"),

    (r"^add-issues/$", login_required(AddIssues.as_view()), {}, "add_issues"),
)
