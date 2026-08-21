from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib import messages

from auth_system.models import CustomUser
from .forms import PhoneAuthenticationForm, UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


@login_required
def index_view(request):
    return render(request, "index.html")


# def register(request):
#     if request.method == "POST":
#         register_form = UserRegistrationForm(request.POST)
#         if register_form.is_valid():
#             register_form.save()
#             return redirect("login")
#         else:
#             messages.error(request, "Дані введені некоректно!")
#             return redirect("register")
#     else:
#         register_form = UserRegistrationForm()
#         return render(request, "auth_system/register.html", context={"register_form": register_form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        login_form = PhoneAuthenticationForm(request, data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            if not user.is_active:
                return redirect("index")
            login(request, user)

            if not login_form.cleaned_data.get("remember_me"):
                request.session.set_expiry(0)

            return redirect("index")

        return render(
            request,
            "auth_system/login.html",
            {
                "login_form": login_form,
            },
        )

    else:
        login_form = PhoneAuthenticationForm()

    return render(request, "auth_system/login.html", {
        "login_form": login_form
    })

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def users_list_view(request):
    q = request.GET.get("q", "").strip()
    clients_qs = CustomUser.objects.all()
    if q:
        clients_qs = clients_qs.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(phone_number__icontains=q)
        )

    user_created = request.GET.get("user_created") == "1"

    paginator = Paginator(clients_qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "auth_system/list.html", {
        "users": page_obj,
        "page_obj": page_obj,
        "user_created": user_created,
    })

@login_required
def user_create_view(request):
    if request.method == "POST":
        create_user_form = UserRegistrationForm(request.POST)
        if create_user_form.is_valid():
            create_user_form.save()
            create_user_form = UserRegistrationForm()
            response = HttpResponse()
            response["HX-Redirect"] = "/auth/users/?user_created=1"
            return response
    else:
        create_user_form = UserRegistrationForm()
    
    return render(request, "auth_system/partials/create_modal.html", context={
        "create_user_form": create_user_form,
        "user_created": request.GET.get("user_created") == "1",
    })

@login_required
def user_update_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == "POST":
        update_user_form = UserUpdateForm(request.POST, instance=user)
        if update_user_form.is_valid():
            update_user_form.save()
            response = HttpResponse()
            response["HX-Redirect"] = "/auth/users/"

            return response
    else:
        update_user_form = UserUpdateForm(instance=user)

    return render(request, "auth_system/partials/update_modal.html", {
        "update_user_form": update_user_form,
        "user": user,
    })

@login_required
def user_delete_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == "POST":
        user.delete()
        response = HttpResponse()
        response["HX-Redirect"] = "/auth/users/"

        return response

    return render(request, "auth_system/partials/delete_modal.html", {
        "user": user
    })