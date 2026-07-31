from datetime import timedelta
import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from appointments.forms import AppointmentForm, MasterFilterForm, StatusFilterForm
from appointments.models import AppointmentModel
from procedures.models import MasterModel, ProcedureModel


def get_appointments_statistics(queryset):
    today = timezone.localdate()

    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=7)

    return queryset.aggregate(
        all_appointments_count=Count("id"),
        week_appointments_count=Count(
            "id",
            filter=Q(
                start_at__date__gte=week_start,
                start_at__date__lt=week_end,
                status="booked",
            ),
        ),
        today_appointments_count=Count(
            "id",
            filter=Q(
                start_at__date=today,
                status="booked",
            ),
        ),
        canceled_appointments_count=Count(
            "id",
            filter=Q(status="canceled"),
        ),
    )


@login_required
def calendar_api_view(request):
    return render(request, "appointments/calendar.html", {
        "masters": MasterModel.objects.filter(is_active=True),
    })


@login_required
def appointments_api_view(request):
    appointments_qs = AppointmentModel.objects.select_related(
        "master", "client", "procedure"
    ).filter(status__in=["booked", "done"])

    master_id = request.GET.get("master")
    if master_id:
        appointments_qs = appointments_qs.filter(master_id=master_id)

    data = []

    for appointment in appointments_qs:
        client_name = f"{appointment.client.last_name} {appointment.client.first_name}"
        master_name = f"{appointment.master.first_name} {appointment.master.last_name}"
        data.append({
            "id": appointment.id,
            "title": client_name,
            "start": appointment.start_at.isoformat(),
            "end": appointment.end_at.isoformat(),

            "extendedProps": {
                "masterId": appointment.master.id,
                "masterName": master_name,
                "clientName": client_name,
                "procedureName": appointment.procedure.title,
                "procedureDuration": appointment.procedure.duration,
                "procedurePrice": appointment.procedure.price,
                "status": appointment.get_status_display(),
                "statusKey": appointment.status,
                "comment": appointment.comment,
            },

            "color":appointment.master.color,
        })

    return JsonResponse(data, safe=False)


@login_required
def appointments_update_view(request, pk):
    appointment = get_object_or_404(AppointmentModel, pk=pk)

    if request.method == "POST":
        update_appointment_form = AppointmentForm(request.POST, instance=appointment)
        if update_appointment_form.is_valid():
            update_appointment_form.save()
            response = HttpResponse()
            response["HX-Trigger"] = json.dumps({"appointment-updated": True})
            response["HX-Redirect"] = ""
            return response
    else:
        update_appointment_form = AppointmentForm(instance=appointment)

    return render(request, "appointments/partials/update_modal.html", {
        "update_appointment_form": update_appointment_form,
        "appointment": appointment,
    })


@login_required
def appointments_delete_view(request, pk):
    appointment = get_object_or_404(AppointmentModel, pk=pk)

    if request.method == "POST":
        appointment.delete()
        response = HttpResponse()
        response["HX-Trigger"] = json.dumps({"appointment-deleted": True})
        return response

    return render(request, "appointments/partials/delete_modal.html", {
        "appointment": appointment,
    })

@login_required
def appointments_cancel_view(request, pk):
    appointment = get_object_or_404(AppointmentModel, pk=pk)

    if request.method == "POST":
        appointment.status = "canceled"
        appointment.save()
        response = HttpResponse()
        response["HX-Trigger"] = json.dumps({"appointment-canceled": True})
        response["HX-Redirect"] = ""

        return response

    return render(request, "appointments/partials/delete_modal.html", {
        "appointment": appointment,
    })

@login_required
def appointments_create_view(request):
    if request.method == "POST":
        create_appointment_form = AppointmentForm(request.POST)
        if create_appointment_form.is_valid():
            create_appointment_form.save()
            response = HttpResponse()
            response["HX-Trigger"] = json.dumps({"appointment-created": True})
            return response
    else:
        create_appointment_form = AppointmentForm()
    return render(request, "appointments/partials/create_modal.html", {
        "create_appointment_form": create_appointment_form,
    })


@login_required
def load_procedures_view(request):
    master_id = request.GET.get("master")

    procedures = ProcedureModel.objects.filter(
        is_active=True,
        procedure_masters__master_id=master_id,
    ).distinct()

    return render(request, "appointments/partials/procedure_options.html", {
            "procedures": procedures,
     })

@login_required
def appointments_list_view(request):
    q = request.GET.get("q", "").strip()
    appointments_qs = AppointmentModel.objects.select_related(
        "master", "client", "procedure"
    ).order_by("-start_at")

    statistics = get_appointments_statistics(appointments_qs)

    status_filter_form = StatusFilterForm(request.GET)
    if status_filter_form.is_valid():
        status = status_filter_form.cleaned_data["status"]
        if status:
            appointments_qs = appointments_qs.filter(status=status)

    master_filter_form = MasterFilterForm(request.GET)
    if master_filter_form.is_valid():
        master = master_filter_form.cleaned_data["master"]
        if master:
            appointments_qs = appointments_qs.filter(master=master)

    if q:
        appointments_qs = appointments_qs.filter(
            Q(client__first_name__icontains=q) |
            Q(client__last_name__icontains=q) |
            Q(client__phone_number__icontains=q) 
        )
    
    paginator = Paginator(appointments_qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "appointments": appointments_qs,
        "page_obj": page_obj,
        **statistics,
        "status_filter_form": status_filter_form,
        "master_filter_form": master_filter_form,
    }

    return render(request, "appointments/list.html", context)