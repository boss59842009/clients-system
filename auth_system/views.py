from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import PhoneAuthenticationForm, UserRegistrationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


@login_required
def index_view(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect("login")
        else:
            messages.error(request, "Дані введені некоректно!")
            return redirect("register")
    else:
        register_form = UserRegistrationForm()
        return render(request, "auth_system/register.html", context={"register_form": register_form})

def login_view(request):
    if request.method == "POST":
        login_form = PhoneAuthenticationForm(request, data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)

            if not login_form.cleaned_data.get("remember_me"):
                request.session.set_expiry(0)

            return redirect("index")

        messages.error(request, "Невірні дані")
        return redirect("login")

    else:
        login_form = PhoneAuthenticationForm()

    return render(request, "auth_system/login.html", {
        "login_form": login_form
    })

def logout_view(request):
    logout(request)
    return redirect('login')