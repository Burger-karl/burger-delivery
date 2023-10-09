from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order
from .forms import StartOrderForm, AssignOrderForm
from django.conf import settings
from payment.models import Payment
from users.models import User

# Create your views here.

def start_delivery(request):
    if request.method == 'POST':
        form = StartOrderForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.buyer = request.user
            var.save()
            request.session['delivery'] = var.pk

            pk = settings.PAYSTACK_PUBLIC_KEY
            amount = 3000
            payment = Payment.objects.create(amount=amount, email=request.user.email, user=request.user)
            payment.save()

            context = {
                'payment':payment,
                'paystack_pub_key':pk,
                'amount_value':payment.amount_value(),
                'amount':amount,
                'var':var
            }
            return render(request, 'payment/make_payment.html', context)
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('start-delivery')
    else:
        form = StartOrderForm()
        context = {'form':form}
        return render(request, 'delivery/start_delivery.html', context)


#for buyer
def active_delivery(request):
    obj = Order.objects.filter(buyer=request.user, is_verified=True)
    context = {'obj':obj}
    return render(request, 'delivery/active_delivery.html', context)


#for buyer
def delivery_history(request):
    obj = Order.objects.filter(buyer=request.user, is_verified=True)
    context = {'obj':obj}
    return render(request, 'delivery/delivery_history.html', context)


#for global admin
def assign_delivery(request, pk):
    obj = Order.objects.get(pk=pk)
    if request.method == 'POST':
        form = AssignOrderForm(request.POST, instance=obj)
        if form.is_valid():
            var = form.save(commit=False)
            var.has_rider = True
            var.save()
            messages.success(request, f'{var.rider} assigned to deliver the package')
            return redirect('delivery-queue')
        else:
            messages.warning(request, 'Somethin went wrong')
            return redirect('delivery-queue')
    else:
        form = AssignOrderForm(instance=obj)
        form.fields['rider'].queryset = User.objects.filter(is_rider=True)
        context = {'form':form, 'obj':obj}
        return render(request, 'delivery/assign_delivery.html', context)


def delivery_queue(request):
    obj = Order.objects.filter(is_verified=True).order_by('-date_created')
    context = {'obj':obj}
    return render(request, 'delivery/delivery_queue.html', context)


# rider delivery queue
def rider_queue(request):
    obj = Order.objects.filter(rider=request.user, is_verified=True)
    context = {'obj':obj}
    return render(request, 'delivery/rider_queue.html', context)


# Complete a delivery
def complete_delivery(request, pk):
    obj = Order.objects.get(pk=pk)
    obj.is_delivered = True
    obj.save()
    messages.success(request, 'Package Delivered')
    print(f'Email sent to {obj.buyer}')
    return redirect('rider-queue')
