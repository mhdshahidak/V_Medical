from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
    path('', views.admin_home, name='adminhome'),
    path('branchdetails', views.branch_details, name='branchdetails'),
    path('add_branch', views.addbranch, name='addbranch'),
    path('staffdetails', views.staff_details, name='staffdetails'),
    path('addstaff', views.add_staff, name="addstaff"),
    path('transfer', views.transfer, name='transfer'),
    path('stock', views.stock, name='stock'),
    path('stocklist', views.stock_list, name='stocklist'),

]
