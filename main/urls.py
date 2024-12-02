from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path("", views.default, name='default'),
    path("playlist/", views.playlist, name='your_playlists'),
    path("search/", views.search, name='search_page'),
    path('logout/', views.logout_view, name='logout'), 
    path('login/', views.login_view, name='logout'), 
    path('restricted/', views.restricted_view, name='restricted'),
    path('signup/', views.signup_view, name='signup'),
    path('admin/', admin.site.urls), 
]