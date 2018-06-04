from django.urls import path, include
from api_data_science_app.v1.analysis import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('api/users', views.UserViewSet)
router.register('api/analyses', views.AnalysisViewSet)

urlpatterns = [
                  path('', include(router.urls)),
              ]