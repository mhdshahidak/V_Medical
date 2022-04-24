from django.urls import path
from . import views

app_name = 'branch'

urlpatterns = [
    path('', views.branch_home, name='branchhome'),
    path('login',views.login,name="login"),
    path('forgotpassword',views.forgotpassword,name="forgotpassword"),
    path('customers', views.customers, name='customers'),
    path('addcustomers', views.addcustomers, name='addcustomers'),
    path('editcustomer/<int:cid>',views.edit_customer,name="editcustomer"),
    path('staff', views.staff, name='staff'),
    path('addstaff', views.add_staff, name='addstaff'),
    path('editstaff/<int:sid>',views.edit_staff,name="editstaff"),
    path('products', views.all_products, name='products'),
    path('addmedicine', views.add_medicine, name='addmedicine'),
    path('billing', views.billing, name='billing'),
    path('bank',views.bank,name="bank"),
    path('addbank', views.add_bank, name='addbank'),
    path('income', views.income, name='income'),
    path('addincome',views.add_income,name="addincome"),
    path('search', views.search_medicine, name='searchmedicine'),
    path('expenses',views.expenses,name='expenses'),
    path('addexpenses',views.add_expenses,name='addexpenses'),
    path('invoicelist', views.invoices_list, name='invoicelist'),
    path('invoicedetails', views.invoices_details, name='invoicedetails'),
    path('editinnvoice',views.edit_innvoice,name="editinnvoice"),
    path('purchaselist',views.purchase_list,name="purchaselist"),
    path('branchprofile', views.branch_profile, name='branchprofile'),
    path('requests', views.med_requests, name='requests'),
    path('profitloss',views.profit_loss,name="profitloss"),
    path('editexpence',views.edit_expence,name="editexpence"),
    path('editproduct',views.edit_product,name="editproduct"),
    path('branchlogout', views.branch_logout, name='branchlogout'),
    



]
