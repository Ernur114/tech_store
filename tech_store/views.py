from rest_framework import generics, permissions
from .models import Category, Product, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer
from django.shortcuts import render, get_object_or_404

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    total_cards = 10
    placeholders_count = max(total_cards - products.count(), 0)
    placeholders = range(placeholders_count)

    order = None
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, is_paid=False)
        order = orders.first() if orders.exists() else None

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
    placeholders_count = max(total_cards - products.count(), 0)
    placeholders = range(placeholders_count)

    order = None
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, is_paid=False)
        order = orders.first() if orders.exists() else None

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
    placeholders_count = max(total_cards - products.count(), 0)
    placeholders = range(placeholders_count)

    order = None
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, is_paid=False)
        order = orders.first() if orders.exists() else None

    return render(request, 'tech_store/catalog.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'placeholders': placeholders,
        'order': order
    })
    

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'tech_store/product_detail.html', {'product': product})

def cart(request):
    order = None
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, is_paid=False)
        order = orders.first() if orders.exists() else None
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

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
