from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Sum, F
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SignUpForm, ProfileForm, ProductForm
from .models import Product, Profile, CartItem, Purchase

# ========== Auth ==========
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # instant login after signup
            messages.success(request, "Welcome to EcoFinds!")
            return redirect("product_list")
    else:
        form = SignUpForm()
    return render(request, "marketplace/signup.html", {"form": form})

@login_required
def dashboard(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("dashboard")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "marketplace/dashboard.html", {"form": form})

# ========== Products ==========
def product_list(request):
    """Browse with keyword search & category filter (title only for MVP)."""
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    products = Product.objects.all()

    if q:
        products = products.filter(title__icontains=q)
    if category:
        products = products.filter(category=category)

    categories = dict(Product._meta.get_field("category").choices)
    return render(request, "marketplace/product_list.html", {
        "products": products,
        "categories": categories,
        "active_category": category,
        "q": q,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "marketplace/product_detail.html", {"product": product})

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.seller = request.user
            prod.save()
            messages.success(request, "Listing created.")
            return redirect("product_detail", pk=prod.pk)
    else:
        form = ProductForm()
    return render(request, "marketplace/product_form.html", {"form": form, "mode": "Create"})

@login_required
def product_update(request, pk):
    prod = get_object_or_404(Product, pk=pk)
    if prod.seller != request.user:
        messages.error(request, "You can edit only your own listings.")
        return redirect("product_detail", pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=prod)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing updated.")
            return redirect("product_detail", pk=pk)
    else:
        form = ProductForm(instance=prod)
    return render(request, "marketplace/product_form.html", {"form": form, "mode": "Edit"})

@login_required
def product_delete(request, pk):
    prod = get_object_or_404(Product, pk=pk)
    if prod.seller != request.user:
        messages.error(request, "You can delete only your own listings.")
        return redirect("product_detail", pk=pk)

    if request.method == "POST":
        prod.delete()
        messages.success(request, "Listing deleted.")
        return redirect("my_listings")
    return render(request, "marketplace/product_delete_confirm.html", {"product": prod})

@login_required
def my_listings(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, "marketplace/my_listings.html", {"products": products})

# ========== Cart & Purchases ==========
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity = F("quantity") + 1
        item.save()
        item.refresh_from_db()
    messages.success(request, f"Added to cart: {product.title}")
    return redirect("cart")

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user).select_related("product")
    total = sum(i.product.price * i.quantity for i in items)
    return render(request, "marketplace/cart.html", {"items": items, "total": total})

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.info(request, "Removed item from cart.")
    return redirect("cart")

@login_required
def checkout(request):
    items = list(CartItem.objects.filter(user=request.user).select_related("product"))
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("cart")

    for it in items:
        Purchase.objects.create(user=request.user, product=it.product, quantity=it.quantity)
    CartItem.objects.filter(user=request.user).delete()
    messages.success(request, "Purchase complete! View your previous purchases.")
    return redirect("purchases")

@login_required
def purchases(request):
    entries = Purchase.objects.filter(user=request.user).select_related("product").order_by("-purchased_at")
    return render(request, "marketplace/purchases.html", {"entries": entries})
