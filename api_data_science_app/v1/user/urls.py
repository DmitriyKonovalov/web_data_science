from django.urls import path, include
from api_data_science_app.v1.user import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', views.UserViewSet)

urlpatterns = [
                  path('', include(router.urls)),
              ]