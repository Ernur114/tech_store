from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, permissions
from .models import Category, Product, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer
from django.contrib.auth.decorators import login_required

def home_view(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    total_cards = 10
    placeholders = range(max(total_cards - products.count(), 0))

    order = None
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, is_paid=False).first()

    return render(request, 'tech_store/index.html', {
        'categories': categories,
        'products': products,
        'placeholders': placeholders,
        'order': order
    })


def catalog_view(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    total_cards = 10
    placeholders = range(max(total_cards - products.count(), 0))

    order = None
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, is_paid=False).first()

    return render(request, 'tech_store/catalog.html', {
        'categories': categories,
        'products': products,
        'placeholders': placeholders,
        'order': order
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    categories = Category.objects.all()
    total_cards = 10
    placeholders = range(max(total_cards - products.count(), 0))

    order = None
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, is_paid=False).first()

    return render(request, 'tech_store/catalog.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'placeholders': placeholders,
        'order': order
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    order, _ = Order.objects.get_or_create(user=request.user, is_paid=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'price': product.price})
    if not created:
        order_item.quantity += 1
        order_item.save()

    order.total_price = sum(item.get_total() for item in order.items.all())
    order.save()
    return redirect('cart')



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    order = None
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, is_paid=False).first()

    return render(request, 'tech_store/product_detail.html', {
        'product': product,
        'order': order
    })


@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, is_paid=False).first()
    return render(request, 'tech_store/cart.html', {'order': order})

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class OrderListAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
