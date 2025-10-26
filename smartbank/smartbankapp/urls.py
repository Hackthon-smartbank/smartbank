from django.urls import path
from . import views
from smartbankapp.login.loginservice import create_new_user,login_get_token
from smartbankapp.customerservice.customer_create import kyc_create,customer_approver,account_creating,customer_deactivate,export_accounts_excel

urlpatterns = [
    path('user_create',create_new_user,name='user_create'),
    path('login_get_token',login_get_token,name='login_get_token'),
    path('kyc_create',kyc_create,name='kyc_create'),
    path('customer_approver',customer_approver,name='customer_approver'),
    path('customer_deactivate',customer_deactivate,name='customer_deactivate'),
    path('account_creating',account_creating,name='account_creating'),
    path('export_accounts_excel',export_accounts_excel,name='export_accounts_excel'),
]