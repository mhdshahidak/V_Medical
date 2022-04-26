import random
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect

from adminapp.models import AdminLogin, Branch, Staff, StaffBankDetails, Transfer
from branch.models import BranchBank, BranchProducts, Customers, Product
from v_med.decorators import auth_branch

# Create your views here.

#login and related
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



#branch dashboard
@auth_branch
def branch_home(request):
    branch=Branch.objects.get(id=request.session['branch'])
    # print(branch.brach_name)
    staff_transfer_request = Transfer.objects.filter(from_branch=branch)
    context={"is_branchhome":True,
        'branch':branch,
        's_transfer':staff_transfer_request
    }
    return render(request,'branch_home.html',context)



# Customers
def customers(request):
    customers=Customers.objects.all().order_by('name')
    branch=Branch.objects.get(id=request.session['branch'])
    context={"is_customers":True,
        'customers':customers,
        'branch':branch
    }
    return render(request,'customers.html',context)


def addcustomers(request):
    branch=Branch.objects.get(id=request.session['branch'])
    if request.method == 'POST':
        customer_name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        place = request.POST['place']

        customer_exist=Customers.objects.filter(name=customer_name,phone=phone).exists()

        if not customer_exist:
            new_customer=Customers(name=customer_name,email=email,phone=phone,place=place)
            new_customer.save()
            return render(request,'addcustomers.html',{'status':1,})

        else:
            context={"is_addcustomers":True,
                "status": 0,
                'branch':branch
            }
            return render(request,'addcustomers.html',context)
    return render(request,'addcustomers.html')



def edit_customer(request,cid):
    branch=Branch.objects.get(id=request.session['branch'])
    if request.method == 'POST':
        customer_name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        place = request.POST['place']
        Customers.objects.filter(id=cid).update(name=customer_name,email=email,phone=phone,place=place)
        return redirect('branch:customers')

    else:
        customers=Customers.objects.get(id=cid)

    context={
        "is_editcustomer":True,
        "customers":customers,
        'branch':branch
        }
    return render(request,'editcustomer.html',context)


def delete_customer(request,cust_delid):
    Customers.objects.filter(id=cust_delid).delete()
    return redirect('branch:customers')

    


# Staff 
def staff(request):
    branch=Branch.objects.get(id=request.session['branch'])
    staffs=StaffBankDetails.objects.filter(staff__branch=request.session['branch'])
    active_staff=StaffBankDetails.objects.filter(staff__branch=request.session['branch'],staff__status='Active')
    print(active_staff)
    inactive_staff=StaffBankDetails.objects.filter(staff__branch=request.session['branch'],staff__status='InActive')
    print(inactive_staff)
    # print(staffs.staff)
    context={"is_staff":True,
        "staffs":staffs,
        'branch':branch,
        'activestaff':active_staff,
        'inactivestaff':inactive_staff,
    }
    return render(request,'staff.html',context)



def add_staff(request):
    rand=random.randint(10000,999999)
    staff_id='VMS'+str(rand)
    profile=""
    
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
        holder_name=request.POST['hname']
        bank_name=request.POST['bname']
        branchname=request.POST['branchname']
        account_num=request.POST['accnum']
        ifsc=request.POST['ifsc']
        
        if request.FILES['profile']:
            profile=request.FILES['profile']

        staff_exist=Staff.objects.filter(name=Name,staff_id=staff_id,phone=phone).exists()

        if not staff_exist:
            new_staff=Staff(profile=profile,name=Name,staff_id=staff_id,email=email,phone=phone,place=place,state=state,address=address,pincode=pincode,date=date,branch=branch)
            new_staff.save()
            new_staff_bank=StaffBankDetails(staff=new_staff,holder_name=holder_name,bank_name=bank_name,account_number=account_num,ifsc=ifsc,branch=branchname)
            new_staff_bank.save()
        return render(request,'addstaff.html',{'status':1,})
   
    else:
        context = {"is_addstaff": True,
            "status":0,
            "branch_id":staff_id
        }
        return render(request,'addstaff.html',context)

    # return render(request,'addstaff.html',context)


def edit_staff(request,sbid,sid):
    print(sbid)
    print(sid)
    staff=request.session['branch']
    print(staff)
    if request.method == 'POST':
        Name = request.POST['name']
        # staff_id = request.POST['id']
        email = request.POST['email']
        phone = request.POST['phone']
        place = request.POST['place']
        state = request.POST['state']
        address = request.POST['address']
        pincode =request.POST['pincode']
        holder_name=request.POST['hname']
        bank_name=request.POST['bname']
        branchname=request.POST['branchname']
        account_num=request.POST['accnum']
        ifsc=request.POST['ifsc']
        # staff=request.session['branch']
        # print(staff)
        # branch= Branch.objects.get(branch=request.session['branch'])
        # print(branch)
        Staff.objects.filter(id=sid).update(name=Name,email=email,phone=phone,place=place,state=state,address=address,pincode=pincode)
        StaffBankDetails.objects.filter(id=sbid).update(holder_name=holder_name,bank_name=bank_name,account_number=account_num,ifsc=ifsc,branch=branchname)
        return redirect('branch:staff')
    else:
        edit_staff=StaffBankDetails.objects.get(id=sbid)
        context={
            "is_editstaff":True,
            "editstaff":edit_staff,
        }
    return render(request,'editstaff.html',context)


def delete_staff(rquest,staff_delid):
    Staff.objects.filter(id=staff_delid).update(status='InActive')
    return redirect('branch:staff')


def getstaffGet(request,sid):

    staffs=StaffBankDetails.objects.get(id=id)

    data={
        "profile":staffs.staff.profile,
        "name":staffs.staff.name,
        "sid":staffs.staff.staff_id,
        "email":staffs.staff.email,
        "phone":staffs.staff.phone,
        # "city":staffs.staff.staff_id,
        "place":staffs.staff.place,
        "address":staffs.staff.address,
        "joindate":staffs.staff.date,
        "branchname":staffs.branch,
        "bankname":staffs.bank_name,
        "accnumber":staffs.account_number,
        "ifsc":staffs.ifsc,

    }
    return JsonResponse({'staff': data})


## Prdouct View functions
def all_products(request):
    products=BranchProducts.objects.filter(branch_id=request.session['branch']).order_by('product__name')
    context={"is_products":True,
        'products':products,
    }
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
                return render(request,'addmedicine.html',{'status':2})
            else:
                medicine = BranchProducts(product=product,quantity=quantity,purchase_date=purchase_date,expiry_date=expiry_date,branch=branch)
                medicine.save()
                return render(request,'addmedicine.html',{'status':1})
        else:
            new_product = Product(product_id=medicine_id,name=name,purchase_cost=p_cost,selling_cost=s_cost,description=description)
            new_product.save()
            branchproduct = BranchProducts(product=new_product,quantity=quantity,purchase_date=purchase_date,expiry_date=expiry_date,branch=branch)
            branchproduct.save()
            msg = "Product Added Successfully"
            return render(request,'addmedicine.html',{'status':1})

    context={"is_addmedicine":True,
        'msg':msg,

    }
    return render(request,'addmedicine.html',context)


def edit_product(request,bpid,prid):
    # print(bpid)
    # print(prid)
    staff=request.session['branch']
    # print(staff)
    # products=BranchProducts.objects.filter(branch_id=request.session['branch'])
    if request.method == 'POST':
        name = request.POST['name']
        quantity = request.POST['quantity']
        p_cost = request.POST['pcost']
        s_cost = request.POST['scost']
        description = request.POST['description']
        branch = Branch.objects.get(id=request.session['branch']) 
        product = Product.objects.get(name=name)
        qproduct = BranchProducts.objects.get(product=product,branch=branch)
        qproduct.quantity = qproduct.quantity + int(quantity)
        qproduct.save()
        BranchProducts.objects.filter(id=bpid).update(branch=branch)
        Product.objects.filter(id=prid).update(name=name,purchase_cost=p_cost,selling_cost=s_cost,description=description)
        return redirect('branch:products')  
    else:
        edit_product=BranchProducts.objects.get(id=bpid)                                   
    context={
        "is_editproduct":True,
        "editproduct":edit_product,
        "status":0,
    }
    return render(request,'editproduct.html',context)


def delete_product(request,pr_delid):
    Product.objects.filter(id=pr_delid).delete()
    return redirect('branch:products')



# billing section
def billing(request):
    product = BranchProducts.objects.filter(branch=request.session['branch'])
    context={"is_billing":True,
        "product":product
    }
    return render(request,'billing.html',context)



# Bank
def bank(request):
    banks=BranchBank.objects.filter(branch=request.session['branch'])
    context={
        "is_bank":True,
        "banks":banks,
        }
    return render(request,'bank.html',context)

def add_bank(request):
    if request.method=='POST':
        holdername=request.POST['accholdername']
        accountnum=request.POST['accnum']
        bankname=request.POST['bankname']
        branchname=request.POST['bname']
        ifsc=request.POST['ifsc']
        branch=Branch.objects.get(id=request.session['branch'])

        new_bank=BranchBank(Accholder_name=holdername,account_number=accountnum,bank_name=bankname,branch_name=branchname,ifsc=ifsc,branch=branch)
        new_bank.save()
    context={
        "is_addbank":True,
        "status":1,
        }
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



def branch_profile(request):
    return render(request,'branchprofile.html')
    

def med_requests(request):
    return render(request,'med_request.html')

def staff_request(request):
    status = "requested"
    branch=Branch.objects.get(id=request.session['branch'])
    staff_transfer_request = Transfer.objects.filter(from_branch=branch,status=status)
    return render(request,'staff_request.html',{'s_transfer':staff_transfer_request,})

def staff_transfer_accept(request,sid):
    status = "accpeted"
    staff_transfer = Transfer.objects.get(id=sid)
    staff_to_transfer=Staff.objects.get(id=staff_transfer.staff.id)
    staff_to_transfer.branch=staff_transfer.to_branch
    staff_transfer.status=status
    staff_to_transfer.save()
    staff_transfer.save()
    

    # Transfer.objects.filter(id=sid).update(staff__branch=staff_transfer.to_branch)
    # staff = Staff.objects.get(staff=staff_transfer.staff)
    # print(staff_transfer)
    # print(staff)
    return redirect('branch:staffrequest')
    


def profit_loss(request):
    context={"is_profitloss":True}
    return render(request,'profit_loss_report.html',context)

def edit_expence(request):
    return render(request,'editexpence.html')


# Purchase list
def purchase_list(request):
    productpurchase = BranchProducts.objects.filter(quantity__lte=100)
    context={
        "is_purchaselist":True,
        "prPurchase":productpurchase,
    }
    return render(request,'purchaselist.html',context)



def branch_logout(request):
    del request.session['branch']
    request.session.flush()
    return redirect('branch:login')

