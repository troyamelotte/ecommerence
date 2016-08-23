from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import User
# Create your views here.
def index(request):
    return render(request, 'grandmashouse/index.html')

def admin(request):

    return render(request, 'grandmashouse/admin.html')

def login(request):
    check = User.userManager.checklog(request.POST['email'], request.POST['pass'])
    if check[0] == True:
        request.session['admin']=User.objects.get(email=request.POST['email']).id
        return redirect('/dashboard/orders')
    else:
        for error in check:
            messages.error(request, error)
        return redirect ('/admin')

def logout(request):
    del request.session['admin']
    return redirect('/admin')

def products(request):
    if not 'admin' in request.session:
        return redirect('/admin')
    return render(request, 'grandmashouse/products.html')

def orders(request):
    if not 'admin' in request.session:
        return redirect('/admin')
    return render(request, 'grandmashouse/orders.html')
