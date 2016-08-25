from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import bcrypt
from django.contrib import messages
import datetime
from .models import User, Product, Order, Category, Ordercontent
# Create your views here.
def index(request):
    if not 'cart' in request.session:
        request.session['cart']=[]
    products_list = Product.objects.all()
    categories = Category.objects.all()
    cartcount = len(request.session['cart'])
    paginator = Paginator(products_list, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'products': products,
        'categories': categories,
        'cartcount':cartcount,
    }
    return render(request, 'grandmashouse/index.html', context)

def filter(request, id):
    products_list = Product.objects.filter(category=Category.objects.get(id=id))
    categories = Category.objects.all()
    paginator = Paginator(products_list, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'grandmashouse/index.html', context)

def ordernew(request, total):
    shippingcheck = Order.orderManager.checkorder(request.POST['sname'], request.POST['saddress'], request.POST['scity'], request.POST['sstate'], request.POST['szipcode'])
    billingcheck =  Order.orderManager.checkorder(request.POST['bname'], request.POST['baddress'], request.POST['bcity'], request.POST['bstate'], request.POST['bzipcode'])
    if shippingcheck == True and billingcheck == True:
        address=str(request.POST['saddress'])+', '+str(request.POST['scity'])+ ', '+str(request.POST['sstate'])+ ', ' +str(request.POST['szipcode'])
        billingaddress = str(request.POST['baddress'])+', '+str(request.POST['bcity'])+ ', '+str(request.POST['bstate'])+ ', ' +str(request.POST['bzipcode'])
        order = Order.objects.create(name=request.POST['sname'], billingname = request.POST['bname'], date = datetime.datetime.now(), address = address, billingaddress=billingaddress, total = total, status = 'In Progress')
        productlist = []
        quantitylist = []

        for item in request.session['cart']:
            productlist.append(item.get('product_id'))
            quantitylist.append(item.get('quantity'))
        for i in range(0,len(productlist)):
            Ordercontent.objects.create(product=Product.objects.get(id=productlist[i]), order = order, quantity = quantitylist[i])
            producterino = Product.objects.get(id=productlist[i])
            val = producterino.sold
            val += quantitylist[i]
            producterino.sold = val
            producterino.save()

        del request.session['cart']
        return redirect('/')
    else:
        for error in shippingcheck:
            messages.error(request, error)
        for error in billingcheck:
            messages.error(request, error)
        return redirect ('/checkout')

def viewproduct(request, id):
    if not 'cart' in request.session:
        request.session['cart']=[]
    product = Product.objects.get(id=id)
    similar = Product.objects.filter(category=product.category).exclude(id=product.id)[:5]
    cartcount = len(request.session['cart'])
    print request.session['cart']
    context = {
        'product':product,
        'similar':similar,
        'cartcount':cartcount,
    }
    return render(request, 'grandmashouse/viewproduct.html', context)

def admin(request):

    return render(request, 'grandmashouse/admin.html')

def addcart(request, id):
    cart = request.session['cart']
    cart.append(dict({'product_id': id, 'quantity': int(request.POST['quantity'])}))
    request.session['cart']=cart
    return redirect('/product/'+str(id))

def deletecart(request):
    del request.session['cart']
    return redirect('/')

def checkout(request):
    cartcount = len(request.session['cart'])
    item_ids = []
    for item in request.session['cart']:
        item_ids.append(int(item.get('product_id')))
    products = Product.objects.filter(id__in=item_ids)
    productlist = []
    itemlist = []
    total = 0;
    for product in products:
        productlist.append(product.price)
    for i in range(0,len(request.session['cart'])):
        itemlist.append(request.session['cart'][i].get('quantity') * productlist[i])
    for cost in itemlist:
        total+=cost
    print itemlist
    totalcard = str(total).replace('.','')
    context = {
        'cartcount':cartcount,
        'products':products,
        'total':total,
        'totalcard':totalcard,

    }
    return render(request, 'grandmashouse/checkout.html', context)
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
    orders_list = Order.objects.all().order_by('-id')
    paginator = Paginator(orders_list, 5)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    context = {
        'orders':orders,
    }
    return render(request, 'grandmashouse/orders.html', context)

def vieworder(request, id):
    order = Order.objects.get(id=id)
    orderitems = Ordercontent.objects.filter(order=order)
    context = {
        'order':order,
        'orderitems':orderitems,
    }
    return render(request, 'grandmashouse/vieworder.html', context)

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
