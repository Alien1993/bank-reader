from rest_framework.routers import DefaultRouter

from .views import MovementViewSet

app_name = "api"

router = DefaultRouter()
router.register(r"movements", MovementViewSet, "movements")

urlpatterns = router.urls
