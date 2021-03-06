from multiprocessing import context
import random
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from branch.models import BranchProducts

from v_med.decorators import auth_admin

from adminapp.models import Branch, Decline, Staff, StaffBankDetails, Transfer

# Create your views here.

@auth_admin
def admin_home(request):
    branches=Branch.objects.all()
    context = {"is_adminhome": True,
        "branches":branches
    }
    return render(request, 'admin_home.html',context)

@auth_admin
def branch_details(request):
    branches=Branch.objects.all()
    active_branch=Branch.objects.filter(status="Active")
    inactive_branch=Branch.objects.filter(status="InActive")
    # print(active_branch)
    context = {"is_branchdetails": True,
                'branches':branches,
                'activebranch':active_branch,
                'inactivebranch':inactive_branch
    }
    return render(request, 'branchdetails.html', context)


@auth_admin
def addbranch(request):
    if Branch.objects.exists():
        branch = Branch.objects.last().id
        branch_id = 'VMID'+str(1000+branch)
    else:
        est=0
        branch_id = 'VMID'+str(1000+est)
    if request.method == 'POST':
        Branch_Name=request.POST['bname']
        branch_id=branch_id
        email=request.POST['email']
        phone=request.POST['phone']
        place=request.POST['place']
        password=request.POST['password']
        address=request.POST['address']
        branch_exist=Branch.objects.filter(branch_name=Branch_Name).exists()
        if not branch_exist:
            new_branch=Branch(branch_name=Branch_Name,branch_id=branch_id,email=email,phone=phone,place=place,address=address,password=password)
            new_branch.save()
            return render(request, 'addbranch.html',{'status':1,})
    else:
        context = {
            "is_addbranch": True,
            "status":0,
        }
        return render(request, 'addbranch.html', context)
    return render(request, 'addbranch.html')
    


@auth_admin
def edit_branch(request,bid):
    if request.method == 'POST':
        branch_Name=request.POST['bname']
        email=request.POST['email']
        phone=request.POST['phone']
        place=request.POST['place']
        address=request.POST['address']
        # branch= Branch.objects.get(id=request.session['branch'])
        Branch.objects.filter(id=bid).update(branch_name=branch_Name,email=email,phone=phone,place=place,address=address)
        return redirect('adminapp:branchdetails')
    else:
        edit_branch=Branch.objects.get(id=bid)
        context={
            "is_editbranch":True,
            "editbranch":edit_branch,
        }
    return render(request,'editbranch.html', context)

@auth_admin
def delete_branch(request,bid):
    status = "InActive"
    branch = Branch.objects.get(id=bid)
    branch.status = status
    branch.save()
    return redirect('adminapp:branchdetails')
   


# staff details
@auth_admin
def staff_details(request):
    staffs = Staff.objects.all()
    # print(staffs)
    active_staff=Staff.objects.filter(status="Active")
    inactive_staff=Staff.objects.filter(status="InActive")
    context = {
        "is_staffdetails": True,
        'staff':staffs,
        "activestaff":active_staff,
        "inactivestaff":inactive_staff,
    }
    return render(request, 'staffdetails.html', context)

@auth_admin
def add_staff(request):
    branch=Branch.objects.all()
    if Staff.objects.exists():
        staff = Staff.objects.last().id
        staff_id = 'VMS'+str(101234+staff)
    else:
        staff=0
        staff_id = 'VMS'+str(101234+staff)
   
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        city=request.POST['city']
        state=request.POST['state']
        branch_id=request.POST['bname']
        phone=request.POST['phone']
        # district=request.POST['dist']
        pincode=request.POST['pincode']
        date=request.POST['joindate']
        address=request.POST['address']
        staffid=staff_id
    
        branch = Branch.objects.get(branch_id=branch_id)
        staff_exist= Staff.objects.filter(name=name,phone=phone).exists()
        if not staff_exist:
            new_staff=Staff(name=name,staff_id=staffid,email=email,phone=phone,place=city,state=state,address=address,date=date,branch=branch,pincode=pincode)
            new_staff.save()
            return render(request, 'add_staff.html',{'status':1,})
        else:
            context = {
            "is_addstaff": True,
            "branch":branch,
            }
            return render(request, 'add_staff.html', context)



    context = {
        "is_addstaff": True,
        "branch":branch,
        }
    return render(request, 'add_staff.html', context)

# def branch_name(request):
#     branchid = request.GET['id']
#     branch = Branch.objects.get(branch_id=branchid)
#     data = {
#         "name":branch.branch_name
#     }
#     return JsonResponse({'staffs': data,})


@auth_admin
def getStaffGet(request,id):
    staffs=Staff.objects.get(id=id)
    staffbank=StaffBankDetails.objects.get(staff__id=id)
    # print(staffs)
    # print(staffbank)
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

@auth_admin
def delete_staff(request,sid):
    status = "InActive"
    staff = Staff.objects.get(id=sid)
    staff.status = status
    staff.save()
    return redirect('adminapp:staffdetails')



# transfer Staff from one branch to another branch
@auth_admin
def transfer(request):
    if request.method == 'POST':
        fbranch = request.POST['from']
        # datatest = request.POST['bfrom']
        tbranch = request.POST['to']
        fdate = request.POST['fdate']
        tdate = request.POST['tdate']

        tstaff = request.POST['sname']
        objfb = Branch.objects.get(branch_name=fbranch)
        objtb = Branch.objects.get(branch_name=tbranch)
        obstaff = Staff.objects.get(id=tstaff)
        send_request = Transfer(staff=obstaff,from_branch=objfb,to_branch=objtb,from_date=fdate,to_date=tdate)
        send_request.save()
        # print(datatest)
        # print(objfb)
        # print(tbranch)
        return render(request, 'transfer.html',{'status':1,})
    staff = Staff.objects.all()
    branch = Branch.objects.all()
    context = {"is_transfer": True,
        'status':0,
        'staff':staff,
        'branch':branch
    }
    return render(request, 'transfer.html', context)


def name_search(request):
    name=request.GET['name']
    staff_data = Staff.objects.filter(branch__branch_name=name)
    # print(staff_data)
    return render(request,'staffnames.html',{'staff_data':staff_data,})


def staff_id(request):
    id=request.GET['id']
    print(id)
    staff_data = Staff.objects.get(id=id)
    # staffid = staff_data.staff_id
    # return render(request,'staffid.html',{'staffid':staffid})
    return render(request,'staffid.html',{'staff_data':staff_data,})


def transfer_history(request):
    message = Decline.objects.all()
    return render(request,'transfer_history.html',{'message':message,})
  


# branch stock list
@auth_admin
def stock(request):
    branch=Branch.objects.all()
    context = {
        "is_stock": True,
        "branches":branch,
    }
    return render(request, 'stock.html', context)



@auth_admin
def stock_list(request,bid):
    branchproduct=BranchProducts.objects.filter(branch=bid)
    print(branchproduct)
    context = {
        "is_stocklist": True,
        "products":branchproduct,
    }
    return render(request, 'stock_list.html', context)

# def admin_logout(request):
#     try:
#         del request.session['admin']
#         request.session.flush()
#         return redirect('branch:login')
#     except:
#         return redirect('branch:login')

@auth_admin
def admin_logout(request):
    del request.session['admin']
    request.session.flush()
    return redirect('branch:login')
       