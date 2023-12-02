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
    path('admindashboard',views.admindashboard,name="admindashboard"),



    #path('admin_index/', views.admin_index, name='admin_index'),
    path('activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),



    path('get_user_data/<str:user_type>/', views.get_user_data, name='get_user_data'),
    # Add other URL patterns as needed


    #path('user',views.user,name='user'),

    path('job_card_application', views.job_card_application, name='job_card_application'),
    path('admin_view_job_cards',views.admin_view_job_cards,name='admin_view_job_cards'),
    path('member',views.member,name='member'),
    path('worker',views.worker,name='worker'),
    path('user',views.user,name='user'),
    path('view_user_jobcard',views.view_user_jobcard,name='view_user_jobcard'),
    path('edit_application<int:job_card_id>', views.edit_application, name='edit_application'),
    path('delete_job_card/<int:job_card_id>/', views.delete_job_card, name='delete_job_card'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('myprofile',views.myprofile,name='myprofile'),
    path('admin_approve_reject<int:job_card_id><str:action>', views.admin_approve_reject, name='admin_approve_reject'),




    path('member_view_worker_list', views.member_view_worker_list, name='member_view_worker_list'),
    path('add_mentor/<int:worker_id>/', views.add_mentor, name='add_mentor'),
    path('remove_mentor/<int:worker_id>/', views.remove_mentor, name='remove_mentor'),


    path('submit-job-card', views.submit_job_card, name='submit_job_card'),

    # URL for taking a job
    path('take-job', views.take_job, name='take_job'),


    path('select_user_job', views.select_user_job, name='select_user_job'),
    path('view_select_user_job', views.view_select_user_job, name='view_select_user_job'),
    path('edit_select_user_job/<int:user_select_job_id>/', views.edit_select_user_job, name='edit_select_user_job'),    path('member_approve_reject/<int:user_selected_job_id>/<str:status>/',views. member_approve_reject, name='member_approve_reject'),

    path('add_job/',views.add_job, name='add_job'),
    path('edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete_job/<int:job_id>', views.delete_job, name='delete_job'),

    #path('accounts/login/', views.login, name='login'),
    path('logout/',views.logout,name="logout"),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]