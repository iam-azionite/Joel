from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .models import Product,Cart,CartItem,Order,OrderItem

# Create your views here.
def products(request):
    products= Product.objects.all()
    return render(request, 'products.html', {'products': products})

@login_required
def cart(request):
    cart,created = Cart.objects.get_or_create(user=request.user)
    cart_items=CartItem.objects.filter(cart=cart)
    total=0
    for item in cart_items:
        total+=item.quantity * item.product.price
    return render(request, 'cart.html', {'cart':cart,'total':total})

@login_required
def add_to_cart(request,id):
    cart,created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=id)
    if products.stock <=0:
        return redirect('products')
    cart_item,created = CartItem.objects.get_or_create(cart=cart,product=product)
    if not created:
        if cart_item.product.stock > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
    return redirect('cart')

@login_required
def increase_quantity(request,id):
    cart_item=CartItem.objects.get(id=id,cart__user=request.user)
    if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def decrease_quantity(request,id):
    cart_item=CartItem.objects.get(id=id,cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required
def remove_from_cart(request,id):
    cart_item=CartItem.objects.get(id=id,cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart,created = Cart.objects.get_or_create(user=request.user)
    cart_items=CartItem.objects.filter(cart=cart)
    total=0
    for item in cart_items:
        total+=item.product.price * item.quantity
    if request.method=='POST':
        for item in cart_items:
            if item.quantity > item.product.stock:
                return render(request,'checkout.html',{'total':total,'cart':cart,'error':f'Not enough stock{item.product.name}'})
        name=request.POST.get('name')
        phone=request.POST.get('phone')
        address=request.POST.get('address')

        order=Order.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            address=address,
            total=total
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart_items.delete()
        return redirect('order_success',id=order.id)
    return render(request,'checkout.html',{'total':total})

@login_required
def order_success(request,id):
    order=Order.objects.get(id=id)
    return render(request,'order_success.html',{'order':order})

@login_required
def my_orders(request):
    order=Order.objects.filter(user=request.user)
    return render(request,'my_orders.html',{'order':order})

@login_required
def order_detail(request,id):
    order=Order.objects.get(id=id)
    order_items=OrderItem.objects.filter(order=order,order__user=request.user)
    return render(request,'order_detail.html',{'order':order,'order_items':order_items})