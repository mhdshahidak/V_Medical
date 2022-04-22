from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request,'login.html')

def forgotpassword(request):
    return render(request,'forgotpassword.html')

def branch_home(request):
    context={"is_branchhome":True}
    return render(request,'branch_home.html',context)

def customers(request):
    context={"is_customers":True}
    return render(request,'customers.html',context)

def addcustomers(request):
    context={"is_addcustomers":True}
    return render(request,'addcustomers.html',context)

def staff(request):
    context={"is_staff":True}
    return render(request,'staff.html',context)

def add_staff(request):
    context={"is_addstaff":True}
    return render(request,'addstaff.html',context)

def all_products(request):
    context={"is_products":True}
    return render(request,'products.html',context)

def add_medicine(request):
    context={"is_addmedicine":True}
    return render(request,'addmedicine.html',context)

def billing(request):
    context={"is_billing":True}
    return render(request,'billing.html',context)

def bank(request):
    context={"is_bank":True}
    return render(request,'bank.html',context)

def add_bank(request):
    context={"is_addbank":True}
    return render(request,'addbank.html',context)

def income(request):
    context={"is_income":True}
    return render(request,'income.html',context)

def add_income(request):
    return render(request,'add_income.html')

def search_medicine(request):
    context={"is_searchmedicine":True}
    return render(request,'search.html',context)

def expenses(request):
    context={"is_expenses":True}
    return render(request,'expenses.html',context)

def add_expenses(request):
    context={"is_addexpenses":True}
    return render(request,'add_expense.html',context)

def invoices_list(request):
    context={"is_invoicelist":True}
    return render(request,'invoices_list.html',context)

def edit_innvoice(request):
    context={"is_editinnvoice":True}
    return render(request,'edit_innvoice.html',context)

def invoices_details(request):
    context={"is_invoicedetails":True}
    return render(request,'invoices_details.html',context)

def purchase_list(request):
    context={"is_purchaselist":True}
    return render(request,'purchaselist.html',context)

def branch_profile(request):
    return render(request,'branchprofile.html')
    

def med_requests(request):
    return render(request,'request.html')

def profit_loss(request):
    context={"is_profitloss":True}
    return render(request,'profit_loss_report.html',context)

def edit_expence(request):
    return render(request,'editexpence.html')

def edit_customer(request):
    return render(request,'editcustomer.html')

def edit_staff(request):
    return render(request,'editstaff.html')

def edit_product(request):
    return render(request,'editproduct.html')

# def view_invoice(request):
#     return render(request,'viewinvoice.html')
