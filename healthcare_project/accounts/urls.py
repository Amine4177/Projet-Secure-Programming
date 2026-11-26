from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import DoctorViewSet, LoginView, PatientViewSet, RegisterView

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patient")
router.register(r"doctors", DoctorViewSet, basename="doctor")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="api-register"),
    path("auth/login/", LoginView.as_view(), name="api-login"),
    path("", include(router.urls)),
]
