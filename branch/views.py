
from datetime import date
import random
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Avg, Min, Max, Count
# from tomlkit import datetime

from django.db.models import F


from adminapp.models import AdminLogin, Branch, Decline, Staff, StaffBankDetails, Transfer
from branch.models import BranchBank, BranchProducts, Customers, Expense, Income, MedicineTransfer, Product
from branch.models import BranchBank, BranchProducts, Customers, Invoive, MedicineTransfer, Product
from v_med.decorators import auth_branch

from datetime import datetime, timedelta, time

# Create your views here.

#login and related
def login(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # admin_exist = AdminLogin.objects.filter(
        #     username=username, password=password).exists()
        branch_exist = Branch.objects.filter(branch_id=username, password=password).exists()
        if username == 'admin' and password == '12345':
            # userDetails = {
            #     'is_admin':True
            # }
            # admin_data = AdminLogin.objects.get(
            #     username=username, password=password)
            # passing customer id as session value

            request.session['admin'] = 'admin'
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
    staff_transfer_request = Transfer.objects.filter(from_branch=branch)

    today = datetime.now().date()
    today_start = datetime.combine(today, time())

    recent_expenses=Expense.objects.filter(branch_id=request.session['branch'],date__gte=today_start)
    recent_invoices=Invoive.objects.select_related('customer').filter(product__branch=request.session['branch'],date__gte=today_start).values('invoice_no','customer__name','date','grand_total').distinct()
    # print(recent_invoices)

    total_income=Income.objects.filter(branch_id__id=request.session['branch'],date__gte=today_start).values('date').aggregate(Sum('incomeamount'))
    # print(total_income)
    total_expense = Expense.objects.filter(branch_id=request.session['branch'],date__gte=today_start).aggregate(Sum('amount'))
    # print(total_expense)
    bank_amount= cash = Invoive.objects.filter(product__branch__id=request.session['branch'],payment_methode="BANK").values('invoice_no','customer__name','grand_total').distinct().aggregate(Sum('grand_total'))
    # print(bank_amount)
    cash = Invoive.objects.filter(product__branch__id=request.session['branch'],payment_methode="CASH").values('invoice_no','customer__name','grand_total').distinct().aggregate(Sum('grand_total'))
    # print(cash)
    upi = Invoive.objects.filter(product__branch__id=request.session['branch'],payment_methode="GOOGLE PAY").values('invoice_no','customer__name','grand_total').distinct().aggregate(Sum('grand_total'))
    staff_count = Staff.objects.filter(branch__id=request.session['branch'],status="Active").values('name','staff_id','status').count()
    # print(total_cash)
    
    context={
        "is_branchhome":True,
        'branch':branch,
        's_transfer':staff_transfer_request,
        'expenses':recent_expenses,
        'invoices':recent_invoices,
        'totalexpense':total_expense,
        'bankamount':bank_amount,
        'cash':cash,
        'upi':upi,
        'staffcount':staff_count,
        'totalincome':total_income,
    }
    return render(request,'branch_home.html',context)



# Customers adding , edit and delete
@auth_branch
def customers(request):
    customers=Customers.objects.all().order_by('name')
    branch=Branch.objects.get(id=request.session['branch'])
    context={
        "is_customers":True,
        'customers':customers,
        'branch':branch
    }
    return render(request,'customers.html',context)


@auth_branch
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
            "branch":branch
        }
    return render(request,'addcustomers.html',context)



@auth_branch
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


@auth_branch
def delete_customer(request,cust_delid):
    Customers.objects.filter(id=cust_delid).delete()
    return redirect('branch:customers')

    


# Staff adding,edit,modal viewing and delete
@auth_branch
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


@auth_branch
def add_staff(request):
    branch=Branch.objects.get(id=request.session['branch'])
    if Staff.objects.exists():
        staff = Staff.objects.last().id
        staff_id = 'VMS'+str(101234+staff)
    else:
        staff=0
        staff_id = 'VMS'+str(101234+staff)
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
        branch = branch
        holder_name=request.POST['hname']
        bank_name=request.POST['bname']
        branchname=request.POST['branchname']
        account_num=request.POST['accnum']
        ifsc=request.POST['ifsc']
        staff_exist=Staff.objects.filter(name=Name,staff_id=staff_id,phone=phone).exists()
        if not staff_exist:
            new_staff=Staff(name=Name,staff_id=staff_id,email=email,phone=phone,place=place,state=state,address=address,pincode=pincode,date=date,branch=branch)
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
            "branch":branch
        }
    return render(request,'addstaff.html',context)


@auth_branch
def edit_staff(request,sbid,sid):
    # print(sbid)
    # print(sid)
    branch=Branch.objects.get(id=request.session['branch'])
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
            "branch":branch
        }
    return render(request,'editstaff.html',context)


@auth_branch
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
@auth_branch
def all_products(request):
    branch = Branch.objects.get(id=request.session['branch'])
    products=BranchProducts.objects.filter(branch_id=request.session['branch']).order_by('product__name')
    context={"is_products":True,
        'products':products,
        "branch":branch
    }
    return render(request,'products.html',context)


@auth_branch
def add_medicine(request):
    branch = Branch.objects.get(id=request.session['branch'])
    if Product.objects.exists():
        product = Product.objects.last().id
        product_id = 'VMSMED'+str(11111+product)
    else:
        product=0
        product_id = 'VMS'+str(101234+staff)

    if request.method == 'POST':
        name = request.POST['name']
        medicine_id = product_id
        quantity = request.POST['quantity']
        p_cost = request.POST['pcost']
        s_cost = request.POST['scost']
        description = request.POST['description']
        purchase_date = request.POST['pdate']
        expiry_date = request.POST['edate']
        branch = branch

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
        "branch":branch
    }
    return render(request,'addmedicine.html',context)


@auth_branch
def edit_product(request,bpid,prid):
    # print(bpid)
    # print(prid)
    branch=Branch.objects.get(id=request.session['branch'])
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
        "branch":branch
    }
    return render(request,'editproduct.html',context)


@auth_branch
def delete_product(request,pr_delid):
    Product.objects.filter(id=pr_delid).delete()
    return redirect('branch:products')



# billing section
@auth_branch
def billing(request):
    if Invoive.objects.exists():
        est = Invoive.objects.last().id
        est_id = 'VMINS'+str(102354+est)
    else:
        est=0
        est_id = 'VMINS'+str(102354+est)
    
    # print(datetime.today())

    product = BranchProducts.objects.filter(branch=request.session['branch'])
    branch = Branch.objects.get(id=request.session['branch'])
    customer = Customers.objects.all()
    context={
        "is_billing":True,
        "product":product,
        "customer":customer,
        "branch":branch,
        "invoice_id":est_id,
    }
    return render(request,'billing.html',context)



@csrf_exempt
def data_adding(request):
    cust_phone = request.POST['customer_phone']
    inv_id = request.POST['invoiceId']
    gst = request.POST['gst']
    grand_total = request.POST['grand_total']
    med_name = request.POST['medicinename']
    qty = request.POST['qty']
    payment_type = request.POST['type']
    item_total = request.POST['itemtotal']
    # print(gst)

    cust_exists = Customers.objects.filter(phone=cust_phone).exists()
    if cust_exists:
        customer = Customers.objects.get(phone=cust_phone)
        product = BranchProducts.objects.get(product__name=med_name,branch=request.session['branch'])
        new_bill = Invoive(invoice_no=inv_id,customer=customer,product=product,quantity=qty,total=item_total,payment_methode=payment_type,gst=gst,grand_total=grand_total)
        # print(new_bill)
        new_bill.save()
        product.quantity = product.quantity - int(qty)
        product.save()
        return JsonResponse({'msg':'BILL GENERATED'})
    return JsonResponse({'msg':'BILL GENERATED'})


@auth_branch
def income_adding_invoice(request):
    grand_total = request.GET['total']
    criteria = "Income from selling"
    catagory = "selling"
    branch = Branch.objects.get(id=request.session['branch'])
    new_income = Income(category=catagory,incomeamount=grand_total,criteria=criteria,branch_id=branch)
    new_income.save()
    return JsonResponse({'msg':'BILL GENERATED'})
    # print(invoice_id)
    


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
    elif not customer_ex:
        new_cust = Customers(phone=phone)
        new_cust.save()
        data={
            "name":new_cust
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


@auth_branch
def preview(request):
    branch = Branch.objects.get(id=request.session['branch'])
    prid = request.GET['prid']
    item_esists = Invoive.objects.filter(invoice_no=prid).exists()
    if item_esists:
        items = Invoive.objects.filter(invoice_no=prid)
        date = Invoive.objects.filter(invoice_no=prid).last()
        cust = Invoive.objects.select_related('customer','product').filter(invoice_no=prid).last()
        total = Invoive.objects.filter(invoice_no=prid).aggregate(Sum('total'))
        totalAmonut = total['total__sum']
        Gst = totalAmonut* 5/100
        final_total = totalAmonut + Gst
        # print(final_total)
                                               
        context={
            "is_billing":True,
            "invid":prid,
            'items':items,
            'cust':cust,
            'date':date,
            'itemtotal':total,
            'gst':Gst,
            'total':final_total ,
            "branch":branch
        }
        return render(request,'preview.html',context)
    else:
        return redirect('branch:billing')


# invoicelist details
@auth_branch
def invoices_list(request):
    branch = Branch.objects.get(id=request.session['branch'])
    invoices=Invoive.objects.values('invoice_no','customer__name','date','grand_total').filter(product__branch=request.session['branch']).annotate(count=Count('invoice_no'),total=Sum('total')).order_by()
    # totalamount = total
    # print(total)
    context={
        "is_invoicelist":True,
        "invoices":invoices,
        "branch":branch,
    }
    return render(request,'invoices_list.html',context)



@auth_branch
def invoices_details(request,id):
    # print(id)
    branch = Branch.objects.get(id=request.session['branch'])
    details = Invoive.objects.filter(invoice_no=id)
    # print(details.invoice_no)
    moredetails = Invoive.objects.filter(invoice_no=id).last()
    sub_total = moredetails.grand_total - moredetails.gst
    print(sub_total)
   
    context={"is_invoicedetails":True,
        "details":details,
        "moredetails":moredetails,
        "sub_total":sub_total,
        "branch":branch,
    }
    return render(request,'invoices_details.html',context)



# search medicine

@auth_branch
def search_medicine(request):
    branch = Branch.objects.get(id=request.session['branch'])
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
    context={
        "is_searchmedicine":True,
        'medicines':medicines,
        "branch":branch,
    }
    return render(request,'search.html',context)



# Bank
@auth_branch
def bank(request):
    branch=Branch.objects.get(id=request.session['branch'])
    banks=BranchBank.objects.filter(branch=request.session['branch'])
    context={
        "is_bank":True,
        "banks":banks,
        "branch":branch,
        }
    return render(request,'bank.html',context)


@auth_branch
def add_bank(request):
    branch=Branch.objects.get(id=request.session['branch'])
    if request.method=='POST':
        holdername=request.POST['accholdername']
        accountnum=request.POST['accnum']
        bankname=request.POST['bankname']
        branchname=request.POST['bname']
        ifsc=request.POST['ifsc']
        branch=branch

        new_bank=BranchBank(Accholder_name=holdername,account_number=accountnum,bank_name=bankname,branch_name=branchname,ifsc=ifsc,branch=branch)
        new_bank.save()
        context={
            "status":1,
        }
    context={
    "is_addbank":True,
    "branch":branch,
    }
    return render(request,'addbank.html',context)
  



#income section
@auth_branch
def income(request):
    branch=Branch.objects.get(id=request.session['branch'])
    income=Income.objects.filter(branch_id=request.session['branch']).all()
    context={
        "is_income":True,
        "income":income,
        "branch":branch,
        }
    return render(request,'income.html',context)


@auth_branch
def add_income(request):
    branch=Branch.objects.get(id=request.session['branch'])
    if request.method=='POST':
        category=request.POST['category']
        date=request.POST['date']
        amount=request.POST['amount']
        criteria=request.POST['criteria']
        # notes=request.POST['notes']
        fromperson=request.POST['fromperson']
        branch=branch
        new_income=Income(category=category,date=date,incomeamount=amount,criteria=criteria,fromperson=fromperson,branch_id=branch)
        new_income.save()
        return render(request,'add_income.html',{'status':1,}) 
    context={
        "is_addincome":True,
        "status":0,
        "branch":branch,
    }
    return render(request,'add_income.html',context)






# Expenses
@auth_branch
def expenses(request):
    branch=Branch.objects.get(id=request.session['branch'])
    expense=Expense.objects.filter(branch_id=request.session['branch'])
    context={
            "is_expenses":True,
            "expense":expense,
            "branch":branch,
        }
    return render(request,'expenses.html',context)


@auth_branch
def add_expenses(request):
    branch=Branch.objects.get(id=request.session['branch'])
    if request.method=='POST':
        category=request.POST['category']
        date=request.POST['date']
        note=request.POST['note']
        amount=request.POST['amount']
        branch=branch

        new_expense=Expense(category=category,date=date,note=note,amount=amount,branch_id=branch)
        new_expense.save()
        return render(request,'add_expense.html',{'status':1,})
    context={
            "is_addexpenses":True,
            "branch":branch
        }
    return render(request,'add_expense.html',context)


@auth_branch
def edit_expence(request,id):
    branch=Branch.objects.get(id=request.session['branch'])
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
    context={
        "branch":branch
    }
    return render(request,'editexpence.html',context)  


@auth_branch
def delete_expense(request,eid):
    Expense.objects.filter(id=eid).delete()
    return redirect('branch:expenses')




@auth_branch
def branch_profile(request):
    return render(request,'branchprofile.html')

# medicine requesting

@auth_branch
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
    context={
        "is_searchmedicine":True,
        'medicines':medicines,
        'msg':msg
    }
    return render(request,'search.html',context)

def medicine_requested(request):
    branch=Branch.objects.get(id=request.session['branch'])
    req_list = MedicineTransfer.objects.filter(reqbranch=request.session['branch'])
    context={
        "is_medicinerequested":True,
        'reqlist':req_list,
        "branch":branch
    }
    return render(request,'medicine_requested.html',context)
    

@auth_branch
def med_requests(request):
    status = "Requested"
    reqformed = MedicineTransfer.objects.filter(avblbranch__branch=request.session['branch'],status=status)
    return render(request,'med_request.html',{'reqformed':reqformed,})

@auth_branch
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

def med_decline(request,pid):
    status = "Rejected"
    medobj = MedicineTransfer.objects.get(id=pid)
    medobj.status =  status 
    medobj.save()
    return redirect('branch:requests')


@auth_branch
def staff_request(request):
    status = "requested"
    branch=Branch.objects.get(id=request.session['branch'])
    staff_transfer_request = Transfer.objects.filter(from_branch=branch,status=status)
    return render(request,'staff_request.html',{'s_transfer':staff_transfer_request,})

@auth_branch
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


def staff_transfer_decline(request):
    msg = request.GET['msg']
    id = request.GET['id']
    status = "Rejected"
    staff_transfer_obj = Transfer.objects.get(id=id)
    staff_transfer_obj.status=status
    staff_transfer_obj.save()
    # print(staff_transfer_obj.status)
    print(id)
    # return redirect('branch:staffrequest')
    
    transfer_obj = Transfer.objects.get(id=id)
    decline = Decline(transfer_id=transfer_obj,msg=msg)
    decline.save()
    return JsonResponse({'msg':'Staff Transfer Declined'})



@auth_branch
def profit_loss(request):
    branch=Branch.objects.get(id=request.session['branch'])
    context={
        "is_profitloss":True,
        "branch":branch
        }
    return render(request,'profit_loss_report.html',context)



def net_profit(request):
    today = datetime.now().date()
    today_start = datetime.combine(today, time())
    print(today_start)
    recent_expenses=Expense.objects.filter(branch_id__id=request.session['branch'],date__gte=today_start).values('id','category','date','amount','expense_type')
    print(recent_expenses)
    recent_income=Income.objects.filter(branch_id__id=request.session['branch'],date__gte=today_start).values('id','category','date','incomeamount','income_type')
    queryset = list(recent_income)+list(recent_expenses)
    print(queryset)
    return JsonResponse({'datas':queryset,})




# Purchase list
@auth_branch
def purchase_list(request):
    branch=Branch.objects.get(id=request.session['branch'])
    productpurchase = BranchProducts.objects.filter(quantity__lte=100)
    context={
        "is_purchaselist":True,
        "prPurchase":productpurchase,
        "branch":branch
    }
    return render(request,'purchaselist.html',context)




@auth_branch
def branch_logout(request):
    del request.session['branch']
    request.session.flush()
    return redirect('branch:login')

