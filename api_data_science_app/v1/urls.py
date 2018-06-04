from django.urls import path, include
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    path("auth/", include("api_data_science_app.v1.auth.urls")),
    path("user/", include("api_data_science_app.v1.user.urls")),
    path("analyses/", include("api_data_science_app.v1.analysis.urls"))
]
