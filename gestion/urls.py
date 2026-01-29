from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExamenViewSet, GroupeAcademiqueViewSet, ResultatViewSet, SoumissionViewSet

router = DefaultRouter()
router.register("examens", ExamenViewSet)
router.register("groupes", GroupeAcademiqueViewSet)
router.register("soumissions", SoumissionViewSet)
router.register("resultats", ResultatViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
