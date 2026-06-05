from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CartAddForm, OrderForm
from .models import Category, OrderItem, Product


def menu(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).select_related('category')
    active = None
    if category_slug:
        active = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active)
    hits = Product.objects.filter(available=True, is_hit=True)[:3]
    return render(request, 'shop/menu.html', {
        'categories': categories,
        'products': products,
        'active_category': active,
        'hits': hits,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related = Product.objects.filter(
        category=product.category, available=True
    ).exclude(id=product.id)[:3]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'add_form': CartAddForm(),
        'related': related,
    })


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, quantity=cd['quantity'], override=cd['override'])
        messages.success(request, f'«{product.name}» добавлено в корзину.')
    return redirect(request.POST.get('next') or 'shop:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('shop:cart_detail')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            return render(request, 'shop/order_done.html', {'order': order})
    else:
        form = OrderForm()
    return render(request, 'shop/checkout.html', {'cart': cart, 'form': form})
