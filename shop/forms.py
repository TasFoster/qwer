from django import forms

from .models import Order


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=50, initial=1)
    override = forms.BooleanField(required=False, initial=False,
                                  widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'address', 'delivery', 'payment', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Как вас зовут?'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (___) ___-__-__'}),
            'address': forms.TextInput(attrs={'placeholder': 'Улица, дом, квартира'}),
            'delivery': forms.RadioSelect,
            'payment': forms.RadioSelect,
            'comment': forms.Textarea(attrs={'rows': 3,
                                             'placeholder': 'Без лука, побольше соуса…'}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('delivery') == 'delivery' and not cleaned.get('address'):
            self.add_error('address', 'Укажите адрес для доставки.')
        return cleaned
