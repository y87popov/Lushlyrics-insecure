from django.contrib import admin
from django.urls import path, include
from main.views import login_view,logout_view, default, signup_view
from main.views import RestrictedView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', default, name='default'),
    path('restricted/', RestrictedView.as_view(), name='restricted'),    
    path('signup/', signup_view, name='signup'),
]
