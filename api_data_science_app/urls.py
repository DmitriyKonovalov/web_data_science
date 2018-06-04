from django.urls import path, include

urlpatterns = [
    path("v1/", include("api_data_science_app.v1.urls"), name="api_v1_auth"),
]
