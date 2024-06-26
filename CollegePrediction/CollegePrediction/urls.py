from django.contrib import admin
from django.urls import path
#from .views import login_view, signup_view
from CollegePrediction import views
from django.contrib.auth import views as auth_views
from .views import custom_logout
# urls.py

from django.urls import path
from .views import prediction_view


urlpatterns = [
    path('predict/', prediction_view, name='prediction'),
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('contact/', views.contact, name='contact'),
    path('home/', views.home_view, name='home'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', custom_logout, name='logout'),

]
