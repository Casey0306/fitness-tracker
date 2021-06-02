from django.conf.urls import url
from .views import RegisterView, VerifyEmail, GetTokenView, RepeatedSentEmailVerifyView


urlpatterns = [
    url('email_register', RegisterView.as_view()),
    url('email_repeated', RepeatedSentEmailVerifyView.as_view()),
    url('email_verify', VerifyEmail.as_view(), name="email-verify"),
    url('get_token', GetTokenView.as_view()),
    ]
