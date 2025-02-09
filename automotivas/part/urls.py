from django.urls import path, include
from rest_framework.routers import DefaultRouter
from part.views import PartViewSet

router = DefaultRouter()
router.register(r'parts', PartViewSet, basename='part')

urlpatterns = [
    path('api/', include(router.urls)),
]

