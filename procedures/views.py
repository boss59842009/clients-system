from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

import procedures
from procedures.forms import MasterForm
from procedures.models import MasterModel, ProcedureModel


def masters_list_view(request):
    q = request.GET.get("q", "").strip()
    masters_qs = MasterModel.objects.all().order_by("-id")
    if q:
        masters_qs = masters_qs.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(phone_number__icontains=q)
        )
    
    paginator = Paginator(masters_qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "masters/list.html", {
        "masters": page_obj,
        "page_obj": page_obj,
    })

def master_detail_view(request, pk):
    master = get_object_or_404(MasterModel, pk=pk)
    procedures = ProcedureModel.objects.filter(masterproceduremodel__master=master).distinct()

    context = {
        "master": master,
        "procedures": procedures,
    }

    return render(request, "masters/detail.html", context)

def master_create_view(request):
    if request.method == "POST":
        create_master_form = MasterForm(request.POST)

        if create_master_form.is_valid():
            create_master_form.save()
            create_master_form = MasterForm()
            return render(request, "masters/partials/create_modal.html", {
                "create_master_form": create_master_form,
                "success": True
            })
    else:
        create_master_form = MasterForm()

    return render(request, "masters/partials/create_modal.html", {
        "create_master_form": create_master_form
    })

def master_update_view(request, pk):
    master = get_object_or_404(MasterModel, pk=pk)

    if request.method == "POST":
        update_master_form = MasterForm(request.POST, instance=master)
        if update_master_form.is_valid():
            update_master_form.save()
            response = HttpResponse()
            response["HX-Redirect"] = "/masters/"

            return response
    else:
        update_master_form = MasterForm(instance=master)

    return render(request, "masters/partials/update_modal.html", {
        "update_master_form": update_master_form,
        "master": master,
    })


def master_delete_view(request, pk):
    master = get_object_or_404(MasterModel, pk=pk)

    if request.method == "POST":
        master.delete()
        response = HttpResponse()
        response["HX-Redirect"] = "/masters/"

        return response

    return render(request, "masters/partials/delete_modal.html", {
        "master": master
    })