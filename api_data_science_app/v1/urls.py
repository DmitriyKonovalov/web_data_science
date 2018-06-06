from django.urls import path, include

from .analysis import urls as analysis_urls
from .auth import urls as auth_urls

urlpatterns = [
    path("auth/", include(auth_urls)),
    path("user/", include("api_data_science_app.v1.user.urls")),
    path("analyses/", include(analysis_urls))
]
