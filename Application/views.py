from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from .models import Order, Service


def home(request):
    return render(request, 'Application/home.html')


def about(request):
    return render(request, 'Application/about.html')


def services(request):
    return render(request, 'Application/services.html')


def contact(request):
    return render(request, 'Application/contact.html')


def pricing(request):
    services = Service.objects.all()
    return render(request, 'Application/pricing.html',
                  {'services': services})


@login_required(login_url='/login/')
def add_to_cart(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    # Filter all pending orders for this user and service
    orders = Order.objects.filter(
        service=service, user=request.user, order_status='Pending')

    if orders.exists():
        # If an order exists, update the first one (or you could merge them)
        order = orders.first()  # Get the first matching order
        order.word_count += 275  # Example increment
        order.total_price = order.word_count * service.price_per_word
        order.save()

        # Optionally, you could delete the other orders if they exist
        if orders.count() > 1:
            orders.exclude(id=order.id).delete()
    else:
        # If no such order exists, create a new one
        Order.objects.create(
            service=service,
            user=request.user,
            deadline=timezone.now() + timezone.timedelta(days=7),  # Example deadline
            word_count=275,  # Example word count
            total_price=service.price_per_word * 275,
            plagiarism_free=service.plagiarism_free,
            revisions=service.revisions,
            order_status='Pending'
        )

    return redirect('cart_view')


@login_required(login_url='/login/')
def remove_from_cart(request, order_id):
    order = get_object_or_404(
        Order, id=order_id, user=request.user, order_status='Pending')
    order.delete()  # Or you can update the status to something else instead of deleting
    return redirect('cart_view')


@login_required(login_url='/login/')
def cart_view(request):
    # Filter orders that belong to the logged-in user and have a status of 'Pending'
    orders = Order.objects.filter(user=request.user, order_status='Pending')

    # Calculate the total price of the orders in the cart
    total_price = sum(order.total_price for order in orders)

    # Define academic levels for the template
    academic_levels = [
        'High School', 'Undergrad. (yrs 1-2)', 'Undergrad. (yrs 3-4)', 'Master\'s', 'PhD']

    # Render the cart template with the user's orders, total price, and academic levels
    return render(request, 'Application/cart.html', {
        'orders': orders,
        'total_price': total_price,
        'academic_levels': academic_levels,
    })


login_required(login_url='/login/')


@login_required(login_url='/login/')
def update_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        academic_level = request.POST.get('academic_level')
        type_of_paper = request.POST.get('type_of_paper')
        other_type = request.POST.get('other_type', '')
        discipline = request.POST.get('discipline')
        instructions = request.POST.get('instructions')
        additional_materials = request.FILES.get('additional_materials')
        deadline = request.POST.get('deadline')

        if order_id:
            order = get_object_or_404(
                Order, id=order_id, user=request.user, order_status='Pending')
            order.academic_level = academic_level
            order.type_of_paper = type_of_paper
            order.other_type = other_type
            order.discipline = discipline
            order.instructions = instructions
            if additional_materials:
                order.additional_materials = additional_materials
            if deadline:
                order.deadline = timezone.make_aware(
                    datetime.strptime(deadline, '%Y-%m-%dT%H:%M'))
            order.save()

        # Redirect to the cart view which handles tabs
        return redirect('cart_view')
    else:
        return redirect('cart_view')


@login_required(login_url='/login/')
def update_pending_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        completion_date = request.POST.get('completion_date')

        if order_id and completion_date:
            order = get_object_or_404(
                Order, id=order_id, user=request.user, order_status='Pending')
            order.deadline = timezone.make_aware(
                datetime.strptime(completion_date, '%Y-%m-%d'))
            order.save()

        return redirect('cart_view')  # Redirect to the cart view with tabs
    else:
        return redirect('cart_view')


@login_required(login_url='/login/')
def pending_orders_view(request):
    # Fetch orders with 'Pending' status for the logged-in user
    orders = Order.objects.filter(user=request.user, order_status='Pending')

    # Render the pending orders template with the orders
    return render(request, 'Application/pending_orders.html', {'orders': orders})
