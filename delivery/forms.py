from django import forms
from .models import Order


class StartOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_name', 'recipient_name', 'recipient_phone', 'recipient_address']


class AssignOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['rider']