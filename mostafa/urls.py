from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('', MostafaViewSet, basename='mostafa')

urlpatterns = router.urls