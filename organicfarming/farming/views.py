import json
import logging
from decimal import Decimal
from decimal import InvalidOperation

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import Order, OrderItem, Product

logger = logging.getLogger(__name__)
# Create your views here.
def index(request):
    return render(request, 'index.html')
def shop(request):
    return render(request, 'shop.html')
def fruit(request):
    return render(request, 'fruit.html' )
def contact(request):
    return render(request, 'contact.html')
def dairy(request):
    return render(request, 'dairy.html')
def dryfruits(request):
    return render(request, 'dryfruits.html')
def about(request):
    return render(request, 'about.html')
def cart(request):
    return render(request, 'cart.html')
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid email or password')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                auth_login(request, user)
                return redirect('index')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'signup.html')
def logout(request):
    auth_logout(request)
    return redirect('index')
def delivery(request):
    delivery_data = {}
    if request.user.is_authenticated:
        last_order = Order.objects.filter(user=request.user).order_by('-created_at').first()
        if last_order:
            delivery_data = {
                'name': last_order.name,
                'phone': last_order.phone,
                'address': last_order.address,
                'city': last_order.city,
                'pincode': last_order.pincode,
            }
        else:
            full_name = request.user.get_full_name() or request.user.username
            if full_name:
                delivery_data['name'] = full_name
    return render(request, 'delivery.html', {'delivery_data': delivery_data})

def payment(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            return JsonResponse({'error': 'You must be logged in to place an order.'}, status=401)
        return redirect(f"{reverse('login')}?next={reverse('payment')}")

    if request.method == "POST":
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        def response_error(message, status=400):
            if is_ajax:
                return JsonResponse({'error': message}, status=status)
            messages.error(request, message)
            return render(request, "payment.html")

        try:
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            address = request.POST.get("address")
            city = request.POST.get("city")
            pincode = request.POST.get("pincode")
            payment_method = request.POST.get("payment")
            total_amount = request.POST.get("total_amount", 0)
            cart_data = request.POST.get('cart_data')

            errors = []
            if not name or not name.strip():
                errors.append('name')
            if not phone or not phone.strip():
                errors.append('phone')
            elif not phone.isdigit() or len(phone.strip()) != 10:
                return response_error('Please enter a valid 10-digit phone number.', status=400)
            if not address or not address.strip():
                errors.append('address')
            if not city or not city.strip():
                errors.append('city')
            if not pincode or not pincode.strip():
                errors.append('pincode')
            elif not pincode.isdigit() or len(pincode.strip()) not in (5, 6):
                return response_error('Please enter a valid pincode.', status=400)
            if not payment_method or not payment_method.strip():
                errors.append('payment method')
            elif payment_method not in ['cod', 'gpay', 'phonepay', 'card']:
                return response_error('Invalid payment method.', status=400)
            if not cart_data:
                errors.append('cart')
            if errors:
                return response_error('Missing or invalid fields: ' + ', '.join(errors), status=400)

            try:
                total_amount = Decimal(str(total_amount)) if total_amount else Decimal('0.00')
            except InvalidOperation:
                return response_error('Invalid total amount.', status=400)

            try:
                items = json.loads(cart_data)
            except json.JSONDecodeError:
                return response_error('Invalid cart data.', status=400)

            if not items:
                return response_error('Cart is empty.', status=400)

            computed_total = Decimal('0.00')
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                phone=phone,
                address=address,
                city=city,
                pincode=pincode,
                payment_method=payment_method,
                total_amount=computed_total
            )

            for item in items:
                product_name = item.get('name', 'Unknown Product')
                item_price = item.get('price', '0.00')
                item_quantity = item.get('quantity', 1) or 1
                try:
                    product_price = Decimal(str(item_price))
                except (InvalidOperation, TypeError, ValueError):
                    product_price = Decimal('0.00')
                try:
                    quantity = int(item_quantity)
                except (TypeError, ValueError):
                    quantity = 1

                computed_total += product_price * quantity
                product, _ = Product.objects.get_or_create(
                    name=product_name,
                    defaults={'price': product_price}
                )

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product_price
                )

            order.total_amount = computed_total
            order.save()

            if is_ajax:
                return JsonResponse({'success': True, 'order_id': order.id})
            return redirect(f"{reverse('order_success')}?order_id={order.id}")
        except Exception as e:
            logger.exception('Payment processing failed')
            if is_ajax:
                if settings.DEBUG:
                    return JsonResponse({'error': f'Internal server error: {e}'}, status=500)
                return JsonResponse({'error': 'Internal server error processing payment. Please try again.'}, status=500)
            if settings.DEBUG:
                messages.error(request, f'Internal server error: {e}')
            else:
                messages.error(request, 'Internal server error processing payment. Please try again.')
            return render(request, "payment.html")

    return render(request, "payment.html")
def order_success(request):
    order_id = request.GET.get('order_id')
    order = None
    if order_id:
        try:
            order = Order.objects.prefetch_related('items__product').get(pk=order_id)
        except Order.DoesNotExist:
            order = None
    return render(request, 'order_success.html', {'order': order})