from django.urls import path
from . import views

app_name = 'adminapp'

urlpatterns = [
    path('', views.admin_home, name='adminhome'),
    path('branchdetails', views.branch_details, name='branchdetails'),
    path('editbranch/<int:bid>', views.edit_branch, name='editbranch'),
    path('deletebranch/<int:bid>', views.delete_branch, name='deletebranch'),
    path('add_branch', views.addbranch, name='addbranch'),
    path('staffdetails', views.staff_details, name='staffdetails'),
    path('getStaffGet/<int:id>',views.getStaffGet,name="getStaffGet"),  
    path('deletestaff/<int:sid>', views.delete_staff, name='deletestaff'),
    path('addstaff', views.add_staff, name="addstaff"),
    path('transfer', views.transfer, name='transfer'),
    path('stock', views.stock, name='stock'),
    path('stocklist/<int:bid>', views.stock_list, name='stocklist'),
    path('adminlogout', views.admin_logout, name='adminlogout'),
    path('namesearch', views.name_search, name="namesearch"),
    path('staffid', views.staff_id, name="staffid"),


]
