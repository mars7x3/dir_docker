from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from dir.models import Resume
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
@login_required(login_url='login')
def cart_add(request, resume_id):
    cart = Cart(request)
    resume = get_object_or_404(Resume, id=resume_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(resume=resume,
                 update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, resume_id):
    cart = Cart(request)
    resume = get_object_or_404(Resume, id=resume_id)
    cart.remove(resume)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart-detail.html', {'cart': cart})


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')
