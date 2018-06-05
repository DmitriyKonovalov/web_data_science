from django.urls import path, include
from rest_framework import routers

from api_data_science_app.v1.analysis import views

router = routers.DefaultRouter()
router.register('', views.AnalysisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
