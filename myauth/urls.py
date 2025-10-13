from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import AboutMeView, ProfileEditView, UserListView, UserDetailView
from . import views

app_name = 'myauth'

urlpatterns = [
    path('about-me/', AboutMeView.as_view(), name='about_me'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('login/', LoginView.as_view(template_name='myauth/login.html', redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('cookie/set/', views.SetCookieView.as_view(), name='set_cookie'),
    path('cookie/get/', views.GetCookieView.as_view(), name='get_cookie'),

    path('session/set/', views.SetSessionView.as_view(), name='set_session'),
    path('session/get/', views.GetSessionView.as_view(), name='get_session'),
]
