
from django import forms

class AddressForm(forms.Form):
    address_name = forms.CharField(max_length=50)
    full_name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=100)
    street_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
    postal_code = forms.CharField(max_length=50)
    is_default = forms.BooleanField(required=False, initial=False)

    def save(self,user,address_instance=None):
        from .models import Address
        data = self.cleaned_data

        if data.get('is_default', False):
            Address.objects.filter(user=user, is_default=True).update(is_default=False)
        if address_instance:
            for field, value in data.items():
                setattr(address_instance,field, value)
            address_instance.save()
            return address_instance
        return Address.objects.create(user=user, **data)


    