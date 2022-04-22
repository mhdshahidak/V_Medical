from multiprocessing import context
import random
from django.shortcuts import render
from django.shortcuts import redirect

from v_med.decorators import auth_admin

from adminapp.models import Branch

# Create your views here.

@auth_admin
def admin_home(request):
    context = {"is_adminhome": True}
    return render(request, 'admin_home.html', context)


def branch_details(request):
    context = {"is_branchdetails": True}
    return render(request, 'branchdetails.html', context)


def addbranch(request):
    msg=""
    rand=random.randint(10000,999999)
    branch_id='VM'+str(rand)
    
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
            msg="ADDED SUCESSFULLY"

        else:
            msg="branch already exist"

    
    context = {"is_addbranch": True,
        "msg":msg,
        "branch_id":branch_id
    
    }


    return render(request, 'addbranch.html', context)

    

    # msg=""
    # rand=random.randint(10000,999999)
    # branch_id='VM'+str(rand)
    
    # if request.method == 'POST':
    #     Branch_Name=request.POST['bname']
    #     branch_id=branch_id
    #     email=request.POST['email']
    #     phone=request.POST['phone']
    #     place=request.POST['place']
    #     password=request.POST['password']
    #     address=request.POST['address']

    #     branch_exist=Branch.objects.filter(branch_name=Branch_Name).exists()

    #     if not branch_exist:
    #         new_branch=Branch(branch_name=Branch_Name,branch_id=branch_id,email=email,phone=phone,place=place,address=address,password=password)
    #         new_branch.save()
    #         msg="ADDED SUCESSFULLY"

    #     else:
    #         msg="branch already exist"


    # return render(request, 'addbranch.html', context)


def staff_details(request):
    context = {"is_staffdetails": True}
    return render(request, 'staffdetails.html', context)


def add_staff(request):
    context = {"is_addstaff": True}
    return render(request, 'add_staff.html', context)


def transfer(request):
    context = {"is_transfer": True}
    return render(request, 'transfer.html', context)


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
