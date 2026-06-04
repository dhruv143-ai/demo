from django.shortcuts import redirect

def client_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('id'):
            return redirect('/client/c_login/')
        return view_func(request, *args, **kwargs)
    return wrapper
from client.decorators import client_login_required

@client_login_required
def update_sub(request):
    # Your view logic here
    pass