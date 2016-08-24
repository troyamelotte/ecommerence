from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import bcrypt
from django.contrib import messages
from .models import User, Product, Order, Category
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
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 5)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
    }
    return render(request, 'grandmashouse/products.html', context)

def orders(request):
    if not 'admin' in request.session:
        return redirect('/admin')
    return render(request, 'grandmashouse/orders.html')

def new(request):
    category = Category.objects.all()

    context = {
        'categories':category,
    }
    return render(request, 'grandmashouse/new.html', context)

def addproduct(request):
    if request.POST['newcat']=='':
        print '*'*50
        category = request.POST['pickcat']
        check = Product.productManager.productcheck(request.POST['name'], request.POST['description'], request.POST['price'], None)
    else:
        print '8'*50
        category = request.POST['newcat']
        check = Product.productManager.productcheck(request.POST['name'], request.POST['description'],request.POST['price'], request.POST['newcat'])
        if check == True:
            Category.objects.create(name=category)
    if check == True:
        print request.FILES['image']
        Product.objects.create(name=request.POST['name'],description=request.POST['description'], category = Category.objects.get(name=category),price = request.POST['price'], image = request.FILES['image'], inventory = request.POST['inventory'])
        return redirect('/dashboard/products')
    for error in check:
        messages.error(request, error)
    return redirect('/new')

def delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('/dashboard/products')

def edit(request, id):
    product = Product.objects.get(id=id)
    category = Category.objects.all()
    print product
    context = {
        'product': product,
        'categories':category,
    }
    return render(request, 'grandmashouse/edit.html', context)

def editproduct(request, id):
    if request.POST['newcat']=='':
        category = request.POST['pickcat']
        check = Product.productManager.editcheck(request.POST['name'], request.POST['description'], request.POST['price'], None)
    else:
        category = request.POST['newcat']
        check = Product.productManager.editcheck(request.POST['name'], request.POST['description'],request.POST['price'], request.POST['newcat'])
        if check == True:
            Category.objects.create(name=category)
    if check == True:
        print request.FILES['image']
        product = Product.objects.get(id=id)
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.category = Category.objects.get(name=category)
        product.price = request.POST['price']
        product.image = request.FILES['image']
        product.inventory = request.POST['inventory']
        product.save()
        return redirect('/dashboard/products')
    for error in check:
        messages.error(request, error)
    return redirect('/edit/'+str(id))
