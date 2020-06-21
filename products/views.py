from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView
from  .models import Tovar, Category, Order, OrderProduct
from django.core.paginator import Paginator
from cart.cart import Cart
from django.conf import settings
import telebot

class CategoryGet:
    """Категории товаров"""
    def get_category(self):
        return Category.objects.all()

class TovarView(CategoryGet, View):
    '''Список товаров'''
    def get(self, request):
        page_number = request.GET.get("page") or 1
        tovar = Tovar.objects.all()
        latest_products = Tovar.objects.order_by("-id")[: 3]
        current_page = Paginator(tovar, 9)
        return render(request, "products/products_list.html", {"products_list": current_page.page(page_number), "paginator": current_page, 'latest_products': latest_products,"categories": self.get_category()})



class TovarDetailView(CategoryGet, View):
    """Полное описание товара"""
    def post(self, request, pk):
        tovar = Tovar.objects.get(id=pk)
        latest_products = Tovar.objects.order_by("-id")[: 3]
        cart = Cart(request)
        cart.add(tovar, tovar.unit_price, request.POST.get('count'))
        count = 0
        for product_in_cart in list(cart):
            if product_in_cart.object_id == pk:
                count = product_in_cart.quantity
        return render(request, "products/products_detail.html",
                      {"products_detail": tovar, 'latest_products': latest_products, "categories": self.get_category(),
                       'count': count})

    def get(self, request, pk):
        tovar = Tovar.objects.get(id = pk)
        latest_products = Tovar.objects.order_by("-id")[: 3]
        cart = Cart(request)
        count=0
        for product_in_cart in list(cart):
            if product_in_cart.object_id == pk:
                count=product_in_cart.quantity
        return render(request, "products/products_detail.html", {"products_detail": tovar, 'latest_products': latest_products, "categories": self.get_category(), 'count': count})

class Search(CategoryGet, ListView):
    """Поиск товаров"""
    def get(self, request):
        products = Tovar.objects.filter(name__icontains=self.request.GET.get("q"))
        latest_products = Tovar.objects.order_by("-id")[: 3]
        return render(request, "products/products_list.html", {"products_list": products, 'latest_products': latest_products, "categories": self.get_category()})

class FilterTovarView(CategoryGet, ListView):
    """Фильтр товаров"""
    def get(self, request):
        product = Tovar.objects.filter(category__in=self.request.GET.getlist("category"))
        latest_products = Tovar.objects.order_by("-id")[: 3]
        return render(request, "products/products_list.html", {"products_list": product, 'latest_products': latest_products, "categories": self.get_category()})

def remove_from_cart(request, product_id):
    product = Tovar.objects.get(id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('/get_cart/')

def get_cart(request):
    cart = Cart(request)
    latest_products = Tovar.objects.order_by("-id")[: 3]
    return render(request, 'cart.html', {'cart': cart, 'summary': cart.summary() ,'latest_products': latest_products,"categories": Category.objects.all()})

def buy(request):
    bot = telebot.TeleBot(settings.TOKEN)
    bot.send_message(settings.TELEGRAM_ID, "Hello")
    cart = Cart(request)
    order = Order.objects.create()
    items = cart.cart.item_set.all()
    for item in items:
        OrderProduct.objects.create(order=order, tovar= Tovar.objects.get(id=item.object_id), kol=item.quantity)
