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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from data_science_app import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('sign_in', auth_views.login, {'template_name': 'sign_in.html'}, name='sign_in'),
                  path('sign_out', auth_views.logout, {'next_page': '/'}, name='sign_out'),
                  path('sign_up/', views.SignUp.as_view(), name='sign_up'),
                  path('user/', login_required(views.UserEdit.as_view()), name='user'),
                  path('', views.home, name='home'),
                  path('desktop', login_required(views.Desktop.as_view()), name='desktop'),
                  path('desktop/<int:pk>', login_required(views.Details.as_view()), name='details'),
                  path('desktop/new_analise', login_required(views.NewAnalysis.as_view()), name='new_analise'),
                  path('desktop/<int:pk>/edit_analise', login_required(views.EditAnalysis.as_view()),
                       name='edit_analise'),
                  path('desktop/<int:pk>/delete', login_required(views.DeleteAnalysis.as_view()), name='delete_analise'),
                  path('desktop/<int:pk>/analize', login_required(views.DoAnalysis.as_view()), name='analize'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
