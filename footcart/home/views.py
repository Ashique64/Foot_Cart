from django.shortcuts import render, redirect, get_object_or_404
from .models import user_details
from django.contrib import messages
from django.contrib.auth import login,logout
from django.views.decorators.cache import never_cache
from . import verify
from admin_page.models import Product,Variants
from django.contrib.auth.decorators import login_required


@never_cache
@login_required(login_url='Login')
def Home(request):
    if request.user.is_superuser:
        logout(request)
        return redirect('Login')
    elif request.user.is_anonymous:
        return redirect('Login')
    else:
        products = Variants.objects.all()[:4]
        return render(request, "home_pages/home.html", {'new_arrivals': products})


@never_cache
def Signup(request):
    if request.method == 'POST':
        name = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password1")
        confirmpassword = request.POST.get("password2")
        if password != confirmpassword:
            messages.warning(request, "Password Doesn't Match")
            return redirect('/Signup')
        try:
            if user_details.objects.get(username=name):
                messages.info(request, "Username Is Already Taken")
                return redirect('/Signup')
        except:
            pass
        try:
            if user_details.objects.get(email=email):
                messages.info(request, "E-mail Is Already Taken")
                return redirect('/Signup')
        except:
            pass
        try:
            if user_details.objects.get(phone=phone):
                messages.info(request, "Phone Number Is Already Taken")
                return redirect('/Signup')
        except:
            pass
        my_user = user_details.objects.create(
            username=name, email=email, phone_number=phone)
        my_user.set_password(password)
        my_user.save()
        login(request, my_user)
        verify.send(my_user.phone_number)
        messages.success(request, "Signup Is Succesfully Please LogIn!.")
        return redirect('Otp', phone, my_user.id)
    return render(request, 'home_pages/signup.html')


@never_cache
def Login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        try:
            user = user_details.objects.get(email=email)
            password_matched = user.check_password(pass1)
        except user_details.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("/Login")

        if user and password_matched:
            login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "home_pages/login.html")

def Logout(request):
    logout(request)
    return redirect('Login')


def Otp(request, phone, id):
    user = get_object_or_404(user_details, id=id)

    if request.method == 'POST':
        code = request.POST.get('otp')

        if verify.check(phone, code):
            user.is_verified = True
            user.save()
            return redirect('/Login')
        else:
            user.delete()
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('/Signup')
    else:
        return render(request, "home_pages/otp.html", {'phone': phone, 'id': id})

@never_cache
def Forget_pass(request):
    if request.method == 'POST':
        phone_number = request.POST.get("reset_phone")
        print(phone_number)

        try:
            user = user_details.objects.get(phone_number=phone_number)
            print(user.phone_number)
            verify.send(user.phone_number)
            return redirect('reset_pass', phone=phone_number, id=user.id)
        except user_details.DoesNotExist:
            messages.error(request, 'User with the given mobile number does not exist.')
            return redirect('Forget_pass')
    
    return render(request, "home_pages/forget_pass.html")

@never_cache
def Reset_pass(request, phone, id):
    user = get_object_or_404(user_details, id=id)

    if request.method == 'POST':
        code = request.POST.get("otp")

        if verify.check(user.phone_number, code):
            user.is_verified = True
            user.save()

            new_password = request.POST.get("password")

            if new_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('Login')
        else:
            messages.error(request, 'Entered OTP is incorrect')

    return render(request, 'home_pages/reset_pass.html', {'phone_number': phone, 'id': id})



