import random
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
# from tomlkit import datetime


from adminapp.models import AdminLogin, Branch, Staff, StaffBankDetails, Transfer
from branch.models import BranchBank, BranchProducts, Customers, Expense, Income, MedicineTransfer, Product
from branch.models import BranchBank, BranchProducts, Customers, Invoive, MedicineTransfer, Product
from v_med.decorators import auth_branch

from django.db.models import Sum,Count

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
    expenses=Expense.objects.filter(branch_id=request.session['branch']).all()
    context={
        "is_branchhome":True,
        'branch':branch,
        's_transfer':staff_transfer_request,
        'expenses':expenses,
    }
    return render(request,'branch_home.html',context)



# Customers
def customers(request):
    customers=Customers.objects.all().order_by('name')
    branch=Branch.objects.get(id=request.session['branch'])
    context={
        "is_customers":True,
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
            context={
                "status": 0,
                'branch':branch
            }
            return render(request,'addcustomers.html',context)
    else:
        context={
            "is_addcustomers":True,
        }
    return render(request,'addcustomers.html',context)




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
    # print(active_staff)
    inactive_staff=StaffBankDetails.objects.filter(staff__branch=request.session['branch'],staff__status='InActive')
    # print(inactive_staff)
    context={
        "is_staff":True,
        "staffs":staffs,
        'branch':branch,
        'activestaff':active_staff,
        'inactivestaff':inactive_staff,
    }
    return render(request,'staff.html',context)



def add_staff(request):
    # rand=random.randint(10000,999999)
    # staff_id='VMS'+str(rand)
    if Staff.objects.exists():
        staff = Staff.objects.last().id
        staff_id = 'VMS'+str(101234+staff)
    else:
        staff=0
        staff_id = 'EST'+str(101234+staff)
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
        if request.POST['profile']:
            profile=request.FILES['profile']
        staff_exist=Staff.objects.filter(name=Name,staff_id=staff_id,phone=phone).exists()
        if not staff_exist:
            new_staff=Staff(profile=profile,name=Name,staff_id=staff_id,email=email,phone=phone,place=place,state=state,address=address,pincode=pincode,date=date,branch=branch)
            new_staff.save()
            new_staff_bank=StaffBankDetails(staff=new_staff,holder_name=holder_name,bank_name=bank_name,account_number=account_num,ifsc=ifsc,branch=branchname)
            new_staff_bank.save()
            return render(request,'addstaff.html',{'status':1,})
        else:
            context = {
                "status":0,
                "branch_id":staff_id
                }
        return render(request,'addstaff.html',context)
    else:
        context={
            "is_addstaff": True,
        }
    return render(request,'addstaff.html',context)



def edit_staff(request,sbid,sid):
    # print(sbid)
    # print(sid)
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


def GetStaffGet(request,id):
    staffs=Staff.objects.get(id=id)
    staffbank=StaffBankDetails.objects.get(staff__id=id)
    print(staffs)
    print(staffbank)
    data={
        "profile":staffs.profile.url,
        "name":staffs.name,
        "staff_id":staffs.staff_id,
        "email":staffs.email,
        "phone":staffs.phone,
        "place":staffs.place,
        "address":staffs.address,
        "date":staffs.date,
        "branch":staffbank.branch,
        "bank_name":staffbank.bank_name,
        "account_number":staffbank.account_number,
        "ifsc":staffbank.ifsc,
    }
    return JsonResponse({'staffs': data,})


## Prdouct View functions
def all_products(request):
    products=BranchProducts.objects.filter(branch_id=request.session['branch']).order_by('product__name')
    context={"is_products":True,
        'products':products,
    }
    return render(request,'products.html',context)



def add_medicine(request):
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
            context={
                'status':0,

            }
            return render(request,'addmedicine.html',context)
    context={
        "is_editproduct":True,
        "editproduct":edit_product,
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
        return render(request,'editproduct.html',{'status':1,})  
    else:
        edit_product=BranchProducts.objects.get(id=bpid)                                   
        context={
            "status":0,
        }
    context={
        "is_editproduct":True,
        "editproduct":edit_product,
    }
    return render(request,'editproduct.html',context)




def delete_product(request,pr_delid):
    Product.objects.filter(id=pr_delid).delete()
    return redirect('branch:products')



# billing section


def billing(request):
    msg = ""
    
    if Invoive.objects.exists():
        est = Invoive.objects.last().id
        est_id = 'VMINS'+str(102354+est)
    else:
        est=0
        est_id = 'VMINS'+str(102354+est)
    
    # print(datetime.today())

    product = BranchProducts.objects.filter(branch=request.session['branch'])
    customer = Customers.objects.all()
    context={"is_billing":True,
        "product":product,
        "customer":customer,
        "invoice_id":est_id,
        "msg":msg,
    }
    return render(request,'billing.html',context)



@csrf_exempt
def data_adding(request):
    
    cust_phone = request.POST['customer_phone']
    inv_id = request.POST['invoiceId']
    med_name = request.POST['medicinename']
    qty = request.POST['qty']
    payment_type = request.POST['type']
    item_total = request.POST['itemtotal']

    cust_exists = Customers.objects.filter(phone=cust_phone).exists()
    if cust_exists:
        customer = Customers.objects.get(phone=cust_phone)
        product = BranchProducts.objects.get(product__name=med_name,branch=request.session['branch'])
        new_bill = Invoive(invoice_no=inv_id,customer=customer,product=product,quantity=qty,total=item_total,payment_methode=payment_type)
        print(new_bill)
        new_bill.save()
        product.quantity = product.quantity - int(qty)
        product.save()

        return JsonResponse({'msg':'BILL GENERATED'})
    
    return JsonResponse({'msg':'BILL GENERATED'})
    # return redirect('branch:billing')
    # return render(request,)


def cust_search(request):
    phone = request.GET['phone']
    customer_ex = Customers.objects.filter(phone=phone).exists()
    print(customer_ex)
    if customer_ex:
        customer = Customers.objects.get(phone=phone)
        data={
            "name":customer.name
        }
        return JsonResponse({'customer':data})
    else:
        pass

def med_price(request):
    med = request.GET['name']
    medlist = Product.objects.get(name=med)
    qtyavlbl = BranchProducts.objects.get(product=medlist.id,branch=request.session['branch'])
    data={
        "price":medlist.selling_cost,
        "maxqty":qtyavlbl.quantity
    }
    return JsonResponse({'product':data,})


def preview(request):
    # context
    try:
        prid = request.GET['prid']
        print(prid)
        items = Invoive.objects.filter(invoice_no=prid)
        date = Invoive.objects.get(invoice_no=prid)
        cust = Invoive.objects.select_related('customer','product').get(invoice_no=prid)
        # sum = Sale.objects.filter(type='Flour').aggregate(Sum('column'))['column__sum']
        # total = Invoive.objects.filter(invoice_no=prid).aggregate(Sum('total'))
        # print(total)

      
        print(items)
        context={"is_billing":True,
            "invid":prid,
            'items':items,
            'cust':cust,
            'date':date

            
        }
        return render(request,'preview.html',context)
    except:
        return  redirect('branch:billing')


# invoices details

def invoices_list(request):
    invoices=Invoive.objects.filter(product__branch=request.session['branch']).all()
    # billed = Invoive.objects.filter(id =invoices).all().count()
    total=Invoive.objects.filter(product__branch=request.session['branch']).aggregate(Sum('total'))
    totalamount=total['total__sum']
    print(totalamount)

    print(totalamount)
    context={
        "is_invoicelist":True,
        "invoices":invoices,
        "total":totalamount,
    }
    return render(request,'invoices_list.html',context)

def edit_innvoice(request):
    context={"is_editinnvoice":True}
    return render(request,'edit_innvoice.html',context)

def invoices_details(request):
    context={"is_invoicedetails":True}
    return render(request,'invoices_details.html',context)


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
        # bankbalane=request.POST['balance']

        new_bank=BranchBank(Accholder_name=holdername,account_number=accountnum,bank_name=bankname,branch_name=branchname,ifsc=ifsc,branch=branch)
        new_bank.save()
        context={
            "status":1,
        }
    context={
    "is_addbank":True,
    }
    return render(request,'addbank.html',context)
  



#income section
def income(request):
    income=Income.objects.filter(branch_id=request.session['branch']).all()
    context={
        "is_income":True,
        "income":income,
        }
    return render(request,'income.html',context)

def add_income(request):
    if request.method=='POST':
        category=request.POST['category']
        date=request.POST['date']
        amount=request.POST['amount']
        criteria=request.POST['criteria']
        # notes=request.POST['notes']
        fromperson=request.POST['fromperson']
        branch=Branch.objects.get(id=request.session['branch'])
        new_income=Income(category=category,date=date,amount=amount,criteria=criteria,fromperson=fromperson,branch_id=branch)
        new_income.save()
        return render(request,'add_income.html',{'status':1,}) 
    context={
        "is_addincome":True,
        "status":0
    }
    return render(request,'add_income.html',context)


# search medicine

def search_medicine(request):
    if request.POST :
        med_name = request.POST['name']
        medicines = Product.objects.all()
        medicine_list = BranchProducts.objects.filter(product__name=med_name)
        # prod = medicine_list.product
        context={"is_searchmedicine":True,
            'medicines':medicines,
            'medicine_list':medicine_list
        }

        return render(request,'search.html',context)
    medicines = Product.objects.all()
    context={"is_searchmedicine":True,
        'medicines':medicines
    }
    return render(request,'search.html',context)



# Expenses
def expenses(request):
    expense=Expense.objects.filter(branch_id=request.session['branch'])
    context={
            "is_expenses":True,
            "expense":expense,
        }
    return render(request,'expenses.html',context)


def add_expenses(request):
    if request.method=='POST':
        category=request.POST['category']
        date=request.POST['date']
        note=request.POST['note']
        amount=request.POST['amount']
        branch=Branch.objects.get(id=request.session['branch'])

        new_expense=Expense(category=category,date=date,note=note,amount=amount,branch_id=branch)
        new_expense.save()
        return render(request,'add_expense.html',{'status':1,})
    context={"is_addexpenses":True}
    return render(request,'add_expense.html',context)

def edit_expence(request,id):
    if request.method=='POST':
        category=request.POST['category']
        date=request.POST['date']
        note=request.POST['note']
        amount=request.POST['amount']
        branch=Branch.objects.get(id=request.session['branch'])
        Expense.objects.filter(id=id).update(category=category,date=date,note=note,amount=amount,branch_id=branch)
    else:
        expense=Expense.objects.get(id=id)
        context = {
            'status':1,
            'expense':expense,
        }
        return render(request,'editexpence.html',context)
    return render(request,'editexpence.html')


def delete_expense(request,eid):
    Expense.objects.filter(id=eid).delete()
    return redirect('branch:expenses')







def branch_profile(request):
    return render(request,'branchprofile.html')

# medicine requesting

def med_requesting(request,pid):

    # avblbranch = request.POST['avblbranch']
    msg = ""
    qty = request.GET['qty']
    avbobj = BranchProducts.objects.get(id=pid)
    reqobj = Branch.objects.get(id=request.session['branch'])

    new_req = MedicineTransfer(reqbranch=reqobj,avblbranch=avbobj,quantity=qty)
    new_req.save()
    msg = "Requested"

    medicines = Product.objects.all()
    context={"is_searchmedicine":True,
        'medicines':medicines,
        'msg':msg
    }
    return render(request,'search.html',context)

def medicine_requested(request):
    req_list = MedicineTransfer.objects.filter(reqbranch=request.session['branch'])
    context={"is_medicinerequested":True,
        'reqlist':req_list
    }
    return render(request,'medicine_requested.html',context)
    

def med_requests(request):
    status = "Requested"
    reqformed = MedicineTransfer.objects.filter(avblbranch__branch=request.session['branch'],status=status)
    return render(request,'med_request.html',{'reqformed':reqformed,})

def med_accept(request,pid):
    medobj = MedicineTransfer.objects.get(id=pid)
    qty = medobj.quantity
    # print(qty)
    branch=BranchProducts.objects.get(id=medobj.avblbranch.id)    #note
    branch.quantity=medobj.avblbranch.quantity-int(qty)
    branch.save()
    medobj.status = "Accepted"
    medobj.save()

    product_exists_in_reqbranch = BranchProducts.objects.filter(product=medobj.avblbranch.product,branch=medobj.reqbranch).exists()
    if not product_exists_in_reqbranch:
        product = medobj.avblbranch.product
        p_date = medobj.avblbranch.purchase_date
        e_date = medobj.avblbranch.expiry_date
        new_qty = medobj.quantity
        req_branch = medobj.reqbranch
        new_product = BranchProducts(product=product,purchase_date=p_date,expiry_date=e_date,quantity=new_qty,branch=req_branch)
        new_product.save()
        
    else:
        added_qty = BranchProducts.objects.get(product=medobj.avblbranch.product,branch=medobj.reqbranch)
        added_qty.quantity = added_qty.quantity + int(qty)
        added_qty.save()

    medobj.save() 
    

    return redirect('branch:requests')

# def med_decline(request,pid):
#     status = "Rejected"
#     medobj = MedicineTransfer.objects.get(id=pid)
#     medobj.status =  status 
#     medobj.save()



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

