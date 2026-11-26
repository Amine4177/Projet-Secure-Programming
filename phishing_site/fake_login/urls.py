from django.urls import path

from . import views

urlpatterns = [
    path("", views.fake_login_view, name="fake-login"),
]
