import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from appointments.forms import AppointmentForm
from appointments.models import AppointmentModel
from procedures.models import MasterModel, ProcedureModel


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