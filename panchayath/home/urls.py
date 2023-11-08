from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('about.html',views.about,name="about"),
    path('service.html',views.service,name="service"),
    path('contact.html',views.contact,name="contact"),
    path('login.html',views.login,name="login"),
    path('registration.html',views.registration,name="registration"),
    #path('index',views.index,name="index"),
    path('dashuser',views.dashuser,name="dashuser"),
    path('dashworker',views.dashworker,name="dashworker"),
    path('dashmember',views.dashmember,name="dashmember"),

    #path('accounts/login/', views.login, name='login'),
    path('logout/',views.logout,name="logout"),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]