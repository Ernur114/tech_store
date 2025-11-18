from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, permissions
from .models import Category, Product, Order, OrderItem
from django.db.models.functions import Lower
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from .forms import ProductForm

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


def search_view(request):
    q = request.GET.get('q', '').strip()
    categories = Category.objects.all()

    order = None
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, is_paid=False).first()

    if q:
        qs = Product.objects.filter(is_active=True)
        products = [p for p in qs if q.casefold() in (p.name or '').casefold()]
        products_count = len(products)
    else:
        products = Product.objects.filter(is_active=True)
        products_count = products.count()

    total_cards = 10
    placeholders = range(max(total_cards - products_count, 0))

    return render(request, 'tech_store/catalog.html', {
        'categories': categories,
        'products': products,
        'placeholders': placeholders,
        'order': order,
        'search_query': q,
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


@login_required
def manage_products(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'tech_store/manage_list.html', {'products': products})


@login_required
def manage_product_create(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manage_products'))
    else:
        form = ProductForm()
    return render(request, 'tech_store/manage_form.html', {'form': form, 'action': 'Создать'})


@login_required
def manage_product_edit(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manage_products'))
    else:
        form = ProductForm(instance=product)
    return render(request, 'tech_store/manage_form.html', {'form': form, 'action': 'Сохранить'})


@login_required
def manage_product_delete(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return HttpResponseRedirect(reverse('manage_products'))
    return render(request, 'tech_store/manage_confirm_delete.html', {'product': product})
