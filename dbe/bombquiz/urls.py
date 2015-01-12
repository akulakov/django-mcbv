from django.conf.urls import *
# from bombquiz.views import Done, Stats, NewPlayer, QV
from bombquiz.views import QuestionView, Done, Stats, NewPlayer

urlpatterns = patterns("bombquiz.views",
    # (r"^question/$" , QV.as_view(), {}, "question"),
    (r"^question/$" , QuestionView.as_view(), {}, "question"),
    (r"^done/$"     , Done.as_view(), {}, "bqdone"),
    (r"^stats/$"    , Stats.as_view(), {}, "stats"),
    (r"^$"          , NewPlayer.as_view(), {}, "new_player"),
)
