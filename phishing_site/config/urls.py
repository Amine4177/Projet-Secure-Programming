from django.urls import include, path

urlpatterns = [
    path("", include("fake_login.urls")),
]
