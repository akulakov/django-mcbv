from django.conf.urls.defaults import *
from dbe.bombquiz.views import *

urlpatterns = patterns("dbe.bombquiz.views",
    (r"^$"          , NewPlayer.as_view(), {}, "new_player"),
    (r"^question/$" , QuestionView.as_view(), {}, "question"),
    (r"^done/$"     , Done.as_view(), {}, "bqdone"),
    (r"^stats/$"    , Stats.as_view(), {}, "stats"),
)
