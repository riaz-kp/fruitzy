from functools import wraps
from django.shortcuts import redirect





def superuser_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_superuser:
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper
