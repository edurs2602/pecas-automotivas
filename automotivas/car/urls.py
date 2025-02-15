from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet

router = DefaultRouter()
router.register(r'', CarViewSet, basename='car')

urlpatterns = [
    path('api/', include(router.urls)),
]

