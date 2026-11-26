from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import EvaluationViewSet

router = DefaultRouter()
router.register(r"evaluations", EvaluationViewSet, basename="evaluation")

urlpatterns = [
    path("", include(router.urls)),
]
