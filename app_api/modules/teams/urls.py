from rest_framework.routers import SimpleRouter

from app_api.modules.teams.views import TeamViewSet

router = SimpleRouter()
router.register('teams', TeamViewSet, basename='team')

urlpatterns = router.urls
