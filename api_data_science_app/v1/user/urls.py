from django.urls import path, include
from rest_framework import routers

from api_data_science_app.v1.user import views

router = routers.DefaultRouter()
router.register('', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
