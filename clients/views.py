from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateClientForm
from .models import ClientModel


def clients_list_view(request):
    create_client_form = CreateClientForm()

    if request.method == "POST":
        create_client_form = CreateClientForm(request.POST)
        if create_client_form.is_valid():
            create_client_form.save()
            messages.success(request, "Клієнта успішно створено.")
            request.session["open_create_modal"] = True  # або ?created=1 в redirect
            return redirect("clients-list")  # PRG — без повторного POST при F5

    open_create_modal = request.session.pop("open_create_modal", False) or (
        request.method == "POST" and not create_client_form.is_valid()
    )
    # після success — чиста форма
    if open_create_modal and request.method == "GET":
        create_client_form = CreateClientForm()

    clients_qs = ClientModel.objects.all().order_by("-id")
    paginator = Paginator(clients_qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "clients/list.html", {
        "clients": page_obj,
        "page_obj": page_obj,
        "create_client_form": create_client_form,
        "open_create_modal": open_create_modal,
    })

def clients_detail_view(request, pk):
    client = get_object_or_404(ClientModel, pk=pk)

    context = {
        "client": client
    }

    return render(request, "clients/detail.html", context)

def clients_update_view(request, id):
    pass


def clients_delete_view(request, pk):
    if request.method == "POST":
        client = get_object_or_404(ClientModel, pk=pk)
        client.delete()

    return redirect("clients-list")