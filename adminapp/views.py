from multiprocessing import context
from django.shortcuts import render
from django.shortcuts import redirect

from v_med.decorators import auth_admin

# Create your views here.

@auth_admin
def admin_home(request):
    context = {"is_adminhome": True}
    return render(request, 'admin_home.html', context)


def branch_details(request):
    context = {"is_branchdetails": True}
    return render(request, 'branchdetails.html', context)


def addbranch(request):
    context = {"is_addbranch": True}
    return render(request, 'addbranch.html', context)


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
