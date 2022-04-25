from multiprocessing import context
import random
from django.shortcuts import render
from django.shortcuts import redirect

from v_med.decorators import auth_admin

from adminapp.models import Branch, Staff, Transfer

# Create your views here.

@auth_admin
def admin_home(request):
    branches=Branch.objects.all()
    context = {"is_adminhome": True,
        "branches":branches
    }

    
    return render(request, 'admin_home.html',context)


def branch_details(request):

    branches=Branch.objects.all()
    context = {"is_branchdetails": True,
                'branches':branches,
    }

    
    return render(request, 'branchdetails.html', context)


def addbranch(request):
    msg=""
    rand=random.randint(10000,999999)
    branchid='VM'+str(rand)
    
    if request.method == 'POST':
        Branch_Name=request.POST['bname']
        branch_id=branchid
        email=request.POST['email']
        phone=request.POST['phone']
        place=request.POST['place']
        password=request.POST['password']
        address=request.POST['address']

        branch_exist=Branch.objects.filter(branch_name=Branch_Name).exists()

        if not branch_exist:
            new_branch=Branch(branch_name=Branch_Name,branch_id=branch_id,email=email,phone=phone,place=place,address=address,password=password)
            new_branch.save()
            msg="ADDED SUCESSFULLY"

        else:
            msg="branch already exist"

    
    context = {"is_addbranch": True,
        "msg":msg,
        # "branch_id":branch_id
    
    }
    return render(request, 'addbranch.html', context)


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


def delete_branch(request,bid):
    status = "InActive"
    branch = Branch.objects.get(id=bid)
    branch.status = status
    branch.save()
    return redirect('adminapp:branchdetails')
   

def staff_details(request):
    staffs = Staff.objects.all()
    context = {"is_staffdetails": True,
        'staff':staffs
    }
    return render(request, 'staffdetails.html', context)


def add_staff(request):
    context = {"is_addstaff": True}
    return render(request, 'add_staff.html', context)


def delete_staff(request,sid):
    status = "InActive"
    staff = Staff.objects.get(id=sid)
    staff.status = status
    staff.save()
    return redirect('adminapp:branchdetails')


def transfer(request):
    if request.method == 'POST':
        fbranch = request.POST['from']
        tbranch = request.POST['to']
        fdate = request.POST['fdate']
        tdate = request.POST['tdate']
        tstaff = request.POST['sname']
        objfb = Branch.objects.get(id=fbranch)
        objtb = Branch.objects.get(id=tbranch)
        obstaff = Staff.objects.get(id=tstaff)
        send_request = Transfer(staff=obstaff,from_branch=objfb,to_branch=objtb,from_date=fdate,to_date=tdate)
        send_request.save()
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
    id=request.GET['id']
    staff_data = Staff.objects.filter(branch=id)
    return render(request,'staffnames.html',{'staff_data':staff_data})

def staff_id(request):
    id=request.GET['id']
    print(id)
    staff_data = Staff.objects.get(id=id)
    # staffid = staff_data.staff_id
    # return render(request,'staffid.html',{'staffid':staffid})
    return render(request,'staffid.html',{'staff_data':staff_data})


def stock(request):
    context = {"is_stock": True}
    return render(request, 'stock.html', context)


def stock_list(request):
    context = {"is_stocklist": True}
    return render(request, 'stock_list.html', context)

def admin_logout(request):
    del request.session['admin']
    request.session.flush()
    return redirect('branch:login')
