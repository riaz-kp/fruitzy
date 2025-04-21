from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
import re
from django.contrib import messages
from .models import userProfile
from category.models import Category



@never_cache
def user_login(request):

    if request.user.is_authenticated:
        return redirect ('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect ('home')
        else:
            messages.error(request, "Username or password is incorrect.")


    return render(request,'user/user_login.html')

def user_signup(request):
    
    if request.user.is_authenticated:
        return redirect ('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        errors = {}

        if any (char.isdigit() or char.isspace() for char in username):
            errors['username_error'] = 'username should not contain numbers or spaces'
            
        if len(username) <4:
            errors['username_error'] ='Username minimum 3 chars required'


        if User.objects.filter(username = username).exists():
            errors['username_error'] ='Username already exits'

        if User.objects.filter(username = email).exists():
            errors['email_error'] ='Email already exits'

        if len(pass1) < 8:
            errors['pssword_error'] = "password atleast 8 charecters long"
        if not re.search(r'[A-Z]', pass1):
            errors['password_error'] = "Password should contain atleast one uppercase letter"
        if not re.search(r'[a-z]', pass1):
            errors['password_error'] = "Password should contain atleast one lowercase letter"
        if not re.search(r'[0-9]', pass1):
            errors['password_error'] = "Password should contain atleast one number"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', pass1):
            errors['password_error'] = 'Password must contain at least one special character'
        
        if pass1 != pass2:
            errors['password_mismatch'] = 'passwords not matching'
        
        if errors:
            return render(request,'user/user_signup.html',{'errors':errors})
        user = User.objects.create_user(username = username, email=email, password=pass1)
        user.save()
        return redirect('user_login')

    return render(request,'user/user_signup.html')



@never_cache
def user_logout(request):
  
    logout(request)
    return redirect('home')


@never_cache
def home(request):

    categories = Category.objects.all()

    return render(request,'user/index.html',{'categories':categories})

def about(request):
    return render(request,'user/about.html')    


def user_management(request):
    # if not request.user.is_authenticated or not request.user.is_superuser:  
    #     return redirect('admin_login') 

    users = User.objects.filter(is_superuser = False).order_by('username')

    return render(request,"admin/users.html",{'users': users})



def block_unblock_user(request,user_id):

    # if not request.user.is_authenticated or not request.user.is_superuser:  
    #     return redirect('admin_login') 

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'block':
            user.is_active = False
        elif action == 'unblock':
            user.is_active = True
        user.save()

    return redirect('user_management')


def custom_404_view(request,exception):
    
    return render(request,'404.html',status=404)


def user_profile(request):
    profile, created = userProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        profile.profile_image = profile_picture
        profile.save()


    return render(request,'user/user_profile.html', {'user':request.user})