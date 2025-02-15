from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

