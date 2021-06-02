from django.conf.urls import url
from .views import SaveUserActivitiesView, GetUserActivitiesView


urlpatterns = [
    url('save_activities', SaveUserActivitiesView.as_view()),
    url(r'^get_activities', GetUserActivitiesView.as_view())
    ]
