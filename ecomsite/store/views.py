from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

# Create your views here


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_item_count = order.total_cart_items
    else:
        items = []
        order = {"total_cart_items": 0, "total_cart_price": 0, "shipping": False}
        cart_item_count = order["total_cart_items"]

    context = {
        "products": Product.objects.all(),
        "cart_item_count": cart_item_count,
        "categories": Category.objects.all(),
    }
    return render(request, "store/store.html", context)


def ProductByCategory(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = category.product_set.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_item_count = order.total_cart_items
    else:
        items = []
        order = {"total_cart_items": 0, "total_cart_price": 0}
        cart_item_count = order["total_cart_items"]
    context = {
        "products": products,
        "category": category,
        "cart_item_count": cart_item_count,
        "categories": Category.objects.all(),
    }
    return render(request, "store/product_by_category.html", context)


def ProductDetail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_item_count = order.total_cart_items
    else:
        items = []
        order = {"total_cart_items": 0, "total_cart_price": 0}
        cart_item_count = order["total_cart_items"]
    context = {
        "product": product,
        "cart_item_count": cart_item_count,
        "categories": Category.objects.all(),
    }
    return render(request, "store/product_detail.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_item_count = order.total_cart_items
    else:
        items = []
        order = {"total_cart_items": 0, "total_cart_price": 0}
        cart_item_count = order["total_cart_items"]
    context = {
        "items": items,
        "order": order,
        "cart_item_count": cart_item_count,
        "shipping": False,
        "categories": Category.objects.all(),
    }
    return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_item_count = order.total_cart_items
    else:
        items = []
        order = {"total_cart_items": 0, "total_cart_price": 0}
        cart_item_count = order["total_cart_items"]
    context = {
        "items": items,
        "order": order,
        "cart_item_count": cart_item_count,
        "shipping": False,
        "categories": Category.objects.all(),
    }
    return render(request, "store/checkout.html", context)


def UpdateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    print("action:", action)
    print(productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderitem.quantity = orderitem.quantity + 1
    elif action == "remove":
        orderitem.quantity = orderitem.quantity - 1
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse("item was added", safe=False)


def ProcessOrder(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data["userForm"]["total"])
        order.transaction_id = transaction_id

        if total == order.total_cart_price:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data["shippingForm"]["address"],
                city=data["shippingForm"]["city"],
                state=data["shippingForm"]["state"],
                zipcode=data["shippingForm"]["zipcode"],
            )

    return JsonResponse("Payment completed", safe=False)
