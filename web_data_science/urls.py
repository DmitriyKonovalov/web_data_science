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
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from data_science_app import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.home, name='home'),
                  path('sign_in',auth_views.login, {'template_name':'sign_in.html'},name='sign_in'),
                  path('sign_up', views.sign_up, name='sign_up'),
                  path('sign_out', auth_views.logout,{'next_page': '/'},name='sign_out'),
                  path('user',views.user_edit, name='user'),
                  path('desktop', views.desktop, name='desktop'),
                  path('desktop/new_analise', views.view_new_analise, name='new_analise'),
                  path('desktop/<int:analise_id>',views.view_detail, name='details'),
                  path('desktop/<int:analise_id>/edit_analise',views.edit_analise, name='edit_analise'),
                  path('desktop/<int:analise_id>/analize',views._analize, name='analize'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
