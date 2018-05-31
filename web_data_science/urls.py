"""web_data_science URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from data_science_app import views, api
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

DEFAULT_LOGIN_URL = '/sign_in'
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('sign_in', auth_views.login, {'template_name': 'sign_in.html'}, name='sign_in'),
                  path('sign_out', auth_views.logout, {'next_page': '/'}, name='sign_out'),
                  path('sign_up/', views.SignUp.as_view(), name='sign_up'),
                  path('user/', login_required(views.UserEdit.as_view(), login_url=DEFAULT_LOGIN_URL), name='user'),
                  path('search', login_required(views.SearchView.as_view(), login_url=DEFAULT_LOGIN_URL),
                       name='search'),
                  path('', login_required(views.Desktop.as_view(), login_url=DEFAULT_LOGIN_URL), name='desktop'),
                  path('desktop', login_required(views.Desktop.as_view(), login_url=DEFAULT_LOGIN_URL), name='desktop'),
                  path('desktop/<int:pk>', login_required(views.Details.as_view(), login_url=DEFAULT_LOGIN_URL),
                       name='details'),
                  path('desktop/new_analysis', login_required(views.NewAnalysis.as_view(), login_url=DEFAULT_LOGIN_URL),
                       name='new_analysis'),
                  path('desktop/<int:pk>/edit_analysis',
                       login_required(views.EditAnalysis.as_view(), login_url=DEFAULT_LOGIN_URL),
                       name='edit_analysis'),
                  path('desktop/<int:pk>/delete',
                       login_required(views.DeleteAnalysis.as_view(), login_url=DEFAULT_LOGIN_URL),
                       name='delete_analysis'),
                  path('desktop/<int:pk>/execute',
                       login_required(views.AnalysisExecute.as_view(), login_url=DEFAULT_LOGIN_URL), name='execute'),
                  path('desktop/<int:pk>/download',
                       login_required(views.DownloadZip.as_view(), login_url=DEFAULT_LOGIN_URL), name='download'),
                  path('api/client/analyses', api.client_get_analysis),
                  path('api/client/users', api.client_get_users),
                  path('api/social', include('rest_framework_social_oauth2.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
