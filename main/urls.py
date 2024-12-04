from django.urls import path
from . import views

urlpatterns = [
    path("", views.default, name='default'),
    path("playlist/", views.playlist, name='your_playlists'),
    path("search/", views.search, name='search_page'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),  # Make sure this maps to login_view correctly
    path('signup/', views.signup_view, name='signup'),  # Signup view path
    path('restricted/', views.restricted_view, name='restricted'),
    path("recover_password/", views.recover_password_view, name='recover_password'),
]