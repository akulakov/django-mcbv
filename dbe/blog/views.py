# Imports {{{
import time
from calendar import month_name

from dbe.blog.models import *
from dbe.blog.forms import *
from dbe.shared.utils import *

from dbe.mcbv.list import ListView
from dbe.mcbv.list_custom import DetailListCreateView
# }}}


class PostView(DetailListCreateView):
    """Show post, associated comments and an 'add comment' form."""
    detail_model    = Post
    list_model      = Comment
    modelform_class = CommentForm
    related_name    = "comments"
    fk_attr         = "post"
    template_name   = "blog/post.html"


class Main(ListView):
    list_model    = Post
    paginate_by   = 10
    template_name = "blog/list.html"

    def months(self):
        """Make a list of months to show archive links."""
        if not Post.obj.count(): return list()

        # set up variables
        current_year, current_month = time.localtime()[:2]
        first       = Post.obj.order_by("created")[0]
        first_year  = first.created.year
        first_month = first.created.month
        months      = list()

        # loop over years and months
        for year in range(current_year, first_year-1, -1):
            start, end = 12, 0
            if year == current_year : start = current_month
            if year == first_year   : end = first_month - 1

            for month in range(start, end, -1):
                if Post.obj.filter(created__year=year, created__month=month):
                    months.append((year, month, month_name[month]))
        return months


class ArchiveMonth(Main):
    paginate_by = None

    def get_list_queryset(self):
        year, month = self.args
        return Post.obj.filter(created__year=year, created__month=month).order_by("created")
