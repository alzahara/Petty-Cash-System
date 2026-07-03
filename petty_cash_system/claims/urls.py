from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='claims/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('employee/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/submit/', views.submit_claim, name='submit_claim'),

    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/action/<int:claim_id>/<str:action>/', views.manager_action, name='manager_action'),

    path('finance/', views.finance_dashboard, name='finance_dashboard'),
    path('finance/action/<int:claim_id>/<str:action>/', views.finance_action, name='finance_action'),

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
