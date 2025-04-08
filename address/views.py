from django.shortcuts import render,redirect,get_object_or_404
from .models import Address
from .forms import AddressForm
# Create your views here.

def manage_address(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'user/address/manage_address.html', {"addresses":addresses})



def add_address(request):
    next_url = request.GET.get('next', 'manage_address')

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect(next_url)
    else:
         form= AddressForm()

    return render(request, 'user/address/add_address.html', {'form':form, 'next_url': next_url})



def edit_address(request,address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)  # Get the address or return 404
    next_url = request.GET.get('next', 'manage_address')  # Default to manage_addresses if no `next` parameter

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save(user=request.user, address_instance=address)  
            return redirect(next_url)  # Redirect to address management page
    else:
        form = AddressForm(initial={
            'address_name': address.address_name,
            'full_name': address.full_name,
            'phone_number': address.phone_number,
            'street_address': address.street_address,
            'postal_code': address.postal_code,
            'is_default': address.is_default,
        })

    return render(request, 'user/address/edit_address.html', {'form': form, 'next_url': next_url})




def delete_address(request,address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    return redirect('manage_address')

def set_default_address(request,address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.set_default()
    return redirect('manage_address')



