import random
from django.shortcuts import render
from django.shortcuts import redirect

from adminapp.models import AdminLogin, Branch, Staff
from branch.models import BranchProducts, Product
from v_med.decorators import auth_branch

# Create your views here.
def login(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        admin_exist = AdminLogin.objects.filter(
            username=username, password=password).exists()
        branch_exist = Branch.objects.filter(branch_id=username, password=password).exists()
        if admin_exist:
            admin_data = AdminLogin.objects.get(
                username=username, password=password)
            # passing customer id as session value
            request.session['admin'] = admin_data.id
            return redirect('adminapp:adminhome')
        elif branch_exist:
            branch = Branch.objects.get(branch_id=username, password=password)
            request.session['branch'] = branch.id
            return redirect('branch:branchhome')
        else:
            msg = "user name or password incorrect"
            return render(request, 'login.html', {'msg':msg,})

    return render(request,'login.html')

def forgotpassword(request):
    return render(request,'forgotpassword.html')

@auth_branch
def branch_home(request):
    branch=Branch.objects.get(id=request.session['branch'])
    # print(branch.brach_name)
    context={"is_branchhome":True,
        'branch':branch
    }
    return render(request,'branch_home.html',context)

def customers(request):
    context={"is_customers":True}
    return render(request,'customers.html',context)

def addcustomers(request):
    context={"is_addcustomers":True}
    return render(request,'addcustomers.html',context)


def staff(request):
    staffs=Staff.objects.filter(branch_id=request.session['branch'])
    context={"is_staff":True,
        "staffs":staffs,
    }
    return render(request,'staff.html',context)

def add_staff(request):
    msg=""
    rand=random.randint(10000,999999)
    staff_id='VMS'+str(rand)
    
    if request.method == 'POST':
        Name = request.POST['name']
        staff_id = staff_id
        email = request.POST['email']
        phone = request.POST['phone']
        place = request.POST['place']
        state = request.POST['state']
        address = request.POST['address']
        pincode = request.POST['pincode']
        date = request.POST['date']
        branch = Branch.objects.get(id=request.session['branch'])

        new_staff=Staff(name=Name,staff_id=staff_id,email=email,phone=phone,place=place,state=state,address=address,pincode=pincode,date=date,branch=branch)
        new_staff.save()
        msg="ADDED SUCESSFULLY"
   
    context = {"is_addstaff": True,
        "msg":msg,
        "branch_id":staff_id
    
    }

    return render(request,'addstaff.html',context)

def all_products(request):
    context={"is_products":True}
    return render(request,'products.html',context)

def add_medicine(request):
    msg = ""
    rand=random.randint(10000,999999)
    product_id='VMP'+str(rand)

    if request.method == 'POST':
        name = request.POST['name']
        medicine_id = product_id
        quantity = request.POST['quantity']
        p_cost = request.POST['pcost']
        s_cost = request.POST['scost']
        description = request.POST['description']
        purchase_date = request.POST['pdate']
        expiry_date = request.POST['edate']
        branch = Branch.objects.get(id=request.session['branch'])

        medicine_exists = Product.objects.filter(name=name).exists()
        if medicine_exists:
            product = Product.objects.get(name=name)
            medicine_in_branch_exists = BranchProducts.objects.filter(product=product,branch=branch).exists()
            if medicine_in_branch_exists:
                qproduct = BranchProducts.objects.get(product=product,branch=branch)
                qproduct.quantity = qproduct.quantity + int(quantity)
                qproduct.save()
                BranchProducts.objects.filter(product=product,branch=branch).update(purchase_date=purchase_date,expiry_date=expiry_date)
                msg = "Stock updated succesfully"
            else:
                medicine = BranchProducts(product=product,quantity=quantity,purchase_date=purchase_date,expiry_date=expiry_date,branch=branch)
                medicine.save()
        else:
            new_product = Product(product_id=medicine_id,name=name,purchase_cost=p_cost,selling_cost=s_cost,description=description)
            new_product.save()
            branchproduct = BranchProducts(product=new_product,quantity=quantity,purchase_date=purchase_date,expiry_date=expiry_date,branch=branch)
            branchproduct.save()
            msg = "Product Added Successfully"

    context={"is_addmedicine":True,
        'msg':msg
    }
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

def branch_logout(request):
    del request.session['branch']
    request.session.flush()
    return redirect('branch:login')

