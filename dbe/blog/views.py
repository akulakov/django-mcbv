# Imports {{{
import time
from calendar import month_name

from blog.models import *
from blog.forms import *
from shared.utils import *

from mcbv.list import ListView
from mcbv.list_custom import DetailListCreateView
# }}}


class PostView(DetailListCreateView):
    """Show post, associated comments and an 'add comment' form."""
    detail_model    = BlogPost
    list_model      = BlogComment
    modelform_class = CommentForm
    related_name    = "comments"
    fk_attr         = "post"
    template_name   = "blog/post.html"


class Main(ListView):
    list_model    = BlogPost
    paginate_by   = 10
    template_name = "blog/list.html"

    def months(self):
        """Make a list of months to show archive links."""
        if not BlogPost.obj.count():
            return list()

        # set up variables
        current_year, current_month = time.localtime()[:2]
        first       = BlogPost.obj.order_by("created")[0]
        first_year  = first.created.year
        first_month = first.created.month
        months      = list()

        # loop over years and months
        for year in range(current_year, first_year-1, -1):
            start, end = 12, 0
            if year == current_year:
                start = current_month
            if year == first_year:
                end = first_month - 1

            for month in range(start, end, -1):
                if BlogPost.obj.filter(created__year=year, created__month=month):
                    months.append((year, month, month_name[month]))
        return months


class ArchiveMonth(Main):
    paginate_by = None

    def get_list_queryset(self):
        year, month = self.args
        return BlogPost.obj.filter(created__year=year, created__month=month).order_by("created")
