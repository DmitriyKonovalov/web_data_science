from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from data_science_app import views

DEFAULT_LOGIN_URL = '/sign_in'

urlpatterns = [path('sign_in', auth_views.login, {'template_name': 'sign_in.html'}, name='sign_in'),
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
                    login_required(views.DownloadZip.as_view(), login_url=DEFAULT_LOGIN_URL), name='download'), ]
