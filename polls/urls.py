from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "polls"
urlpatterns = [
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:pk>/followup/", views.followupquestionDisplay, name="followup"),
    path("new-poll", views.NewPoll.as_view(), name="create_poll"),
    path("<int:pk>/", views.PollDetail.as_view(), name="detail"),
    path("", views.PollList.as_view(), name="index"),

]

urlpatterns = format_suffix_patterns(urlpatterns)