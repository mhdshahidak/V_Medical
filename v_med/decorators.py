from django.shortcuts import redirect

def auth_admin(func):
    def wrap(request, *args, **kwargs):
        if 'admin' in request.session:
            return func(request, *args, **kwargs)
        else:
            return redirect('branch:login')
            
    return wrap