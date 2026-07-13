from django.contrib import auth
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

import appointments
from appointments.models import AppointmentModel
from procedures.forms import MasterForm, ProcedureForm
from procedures.models import MasterModel, MasterProcedureModel, ProcedureModel


"""MASTERS"""
@login_required
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

@login_required
def master_detail_view(request, pk):
    master = get_object_or_404(MasterModel, pk=pk)
    procedure_ids = MasterProcedureModel.objects.filter(
    master=master
    ).values_list("procedure_id", flat=True)

    procedures = ProcedureModel.objects.filter(
        is_active=True,
        id__in=procedure_ids
    )

    appointments =(AppointmentModel.objects.filter(master=master)
        .select_related("client", "procedure")
        .order_by("-start_at")
    )

    context = {
        "master": master,
        "procedures": procedures,
        "all_procedures": ProcedureModel.objects.filter(is_active=True),
        "assigned_ids": set(procedures.values_list("id", flat=True)),
        "appointments": appointments,
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
        "create_master_form": create_master_form,
    })

@login_required
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

@login_required
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

"""PROCEDURES"""
@login_required
def procedures_list_view(request):
    q = request.GET.get("q", "").strip()
    procedures_qs = ProcedureModel.objects.all().order_by("-updated_at")
    if q:
        procedures_qs = procedures_qs.filter(
            Q(title__icontains=q)
        )
    
    paginator = Paginator(procedures_qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "procedures/list.html", {
        "procedures": page_obj,
        "page_obj": page_obj,
    })

@login_required
def procedure_detail_view(request, pk):
    procedure = get_object_or_404(ProcedureModel, pk=pk)
    masters = MasterModel.objects.filter(master_procedures__procedure=procedure).distinct()

    context = {
        "procedure": procedure,
        "masters": masters,
    }

    return render(request, "procedures/detail.html", context)

@login_required
def procedure_create_view(request):
    if request.method == "POST":
        create_procedure_form = ProcedureForm(request.POST)

        if create_procedure_form.is_valid():
            create_procedure_form.save()
            create_procedure_form = ProcedureForm()
            return render(request, "procedures/partials/create_modal.html", {
                "create_procedure_form": create_procedure_form,
                "success": True
            })
    else:
        create_procedure_form = ProcedureForm()

    return render(request, "procedures/partials/create_modal.html", {
        "create_procedure_form": create_procedure_form
    })

@login_required
def procedure_update_view(request, pk):
    procedure = get_object_or_404(ProcedureModel, pk=pk)

    if request.method == "POST":
        update_procedure_form = ProcedureForm(request.POST, instance=procedure)
        if update_procedure_form.is_valid():
            update_procedure_form.save()
            response = HttpResponse()
            response["HX-Redirect"] = "/procedures/"

            return response
    else:
        update_procedure_form = ProcedureForm(instance=procedure)

    return render(request, "procedures/partials/update_modal.html", {
        "update_procedure_form": update_procedure_form,
        "procedure": procedure,
    })

@login_required
def procedure_soft_delete_view(request, pk):
    procedure = get_object_or_404(ProcedureModel, pk=pk)

    if request.method == "POST":
        procedure.is_active = False
        procedure.save()
        response = HttpResponse()
        response["HX-Redirect"] = "/procedures/"

        return response

    return render(request, "procedures/partials/delete_modal.html", {
        "procedure": procedure
    })

@login_required
def add_master_procedures(request, pk):
    master = get_object_or_404(MasterModel, pk=pk)

    if request.method == "POST":
        procedure_ids = request.POST.getlist("procedures")

        # safety guard
        if not procedure_ids:
            procedure_ids = []

        MasterProcedureModel.objects.filter(master=master).delete()

        active_procedure_ids = set(
            ProcedureModel.objects.filter(
                is_active=True,
                id__in=procedure_ids,
            ).values_list("id", flat=True)
        )

        MasterProcedureModel.objects.bulk_create([
            MasterProcedureModel(
                master=master,
                procedure_id=pid,
            )
            for pid in active_procedure_ids
        ])

        procedure_ids = MasterProcedureModel.objects.filter(
            master=master
        ).values_list("procedure_id", flat=True)

        procedures = ProcedureModel.objects.filter(
            id__in=procedure_ids
        )

        response = HttpResponse()
        response["HX-Redirect"] = f"/master/{master.pk}/"

        return response

    return HttpResponse(status=405)