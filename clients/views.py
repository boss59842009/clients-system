from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ClientForm
from .models import ClientModel

@login_required
def clients_list_view(request):
    q = request.GET.get("q", "").strip()
    clients_qs = ClientModel.objects.all().order_by("-id")
    if q:
        clients_qs = clients_qs.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(phone_number__icontains=q) |
            Q(tg__icontains=q)
        )

    clients_count = clients_qs.count()
    active_clients_count = ClientModel.objects.filter(is_active=True).count()
    
    paginator = Paginator(clients_qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "clients/list.html", {
        "clients": page_obj,
        "page_obj": page_obj,
        "clients_count": clients_count,
        "active_clients_count": active_clients_count,
    })

@login_required
def clients_detail_view(request, pk):
    client = get_object_or_404(ClientModel, pk=pk)

    context = {
        "client": client
    }

    return render(request, "clients/detail.html", context)

@login_required
def client_create_view(request):
    if request.method == "POST":
        create_client_form = ClientForm(request.POST)

        if create_client_form.is_valid():
            create_client_form.save()
            create_client_form = ClientForm()
            return render(request, "clients/partials/create_client_modal.html", {
                "create_client_form": create_client_form,
                "success": True
            })
    else:
        create_client_form = ClientForm()

    return render(request, "clients/partials/create_client_modal.html", {
        "create_client_form": create_client_form
    })

@login_required
def clients_update_view(request, pk):
    client = get_object_or_404(ClientModel, pk=pk)

    if request.method == "POST":
        update_client_form = ClientForm(request.POST, instance=client)
        if update_client_form.is_valid():
            update_client_form.save()
            response = HttpResponse()
            response["HX-Redirect"] = "/clients/"

            return response
    else:
        update_client_form = ClientForm(instance=client)

    return render(request, "clients/partials/update_client_modal.html", {
        "update_client_form": update_client_form,
        "client": client
    })

@login_required
def clients_delete_view(request, pk):
    client = get_object_or_404(ClientModel, pk=pk)

    if request.method == "POST":
        client.delete()
        response = HttpResponse()
        response["HX-Redirect"] = "/clients/"

        return response

    return render(request, "clients/partials/delete_client_modal.html", {
        "client": client
    })