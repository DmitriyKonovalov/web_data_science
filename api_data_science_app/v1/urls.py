from django.urls import path, include

urlpatterns = [
    path("auth/", include("api_data_science_app.v1.auth.urls"), name="api_v1_auth"),
    path("analysis/", include("api_data_science_app.v1.analysis.urls"), name="api_v1_analysis")
]