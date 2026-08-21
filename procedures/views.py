import pandas as pd
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
    
    master_created = request.GET.get("master_created") == "1"
    
    paginator = Paginator(masters_qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "masters/list.html", {
        "masters": page_obj,
        "page_obj": page_obj,
        "master_created": master_created
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

    appointments = (AppointmentModel.objects.filter(master=master)
        .select_related("client", "procedure")
        .filter(status="booked")
        .order_by("-start_at")
    )

    paginator = Paginator(appointments, 5)
    page_obj = paginator.get_page(request.GET.get("page"))


    context = {
        "master": master,
        "procedures": procedures,
        "all_procedures": ProcedureModel.objects.filter(is_active=True),
        "assigned_ids": set(procedures.values_list("id", flat=True)),
        "appointments": page_obj,
        "page_obj": page_obj,
    }

    return render(request, "masters/detail.html", context)

@login_required
def master_create_view(request):
    if request.method == "POST":
        create_master_form = MasterForm(request.POST)
        if create_master_form.is_valid():
            create_master_form.save()
            create_master_form = MasterForm()
            response = HttpResponse()
            response["HX-Redirect"] = "/masters/?master_created=1"
            return response
    else:
        create_master_form = MasterForm()

    return render(request, "masters/partials/create_modal.html", {
        "create_master_form": create_master_form,
        "master_created": request.GET.get("master_created") == "1",
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
    import_result = request.session.pop("import_result", None)
    procedure_created = request.GET.get("procedure_created") == "1"


    return render(request, "procedures/list.html", {
        "procedures": page_obj,
        "page_obj": page_obj,
        "import_result": import_result,
        "procedure_created": procedure_created
    })

"""PROCEDURES"""
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
            response = HttpResponse()
            response["HX-Redirect"] = "/procedures/?procedure_created=1"
            return response
    else:
        create_procedure_form = ProcedureForm()

    return render(request, "procedures/partials/create_modal.html", {
        "create_procedure_form": create_procedure_form,
        "procedure_created": request.GET.get("procedure_created") == "1",
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

@login_required
def import_procedures_view(request):
    if request.method != "POST":
        return render(
            request,
            "procedures/partials/import_modal.html",
        )

    excel_file = request.FILES.get("excel_file")

    if not excel_file:
        request.session["import_result"] = {
            "summary": "Файл для імпорту не вибрано.",
            "total": 0,
            "imported": 0,
            "skipped": 0,
            "errors": ["Файл для імпорту не вибрано."],
        }
        return redirect("procedures-list")

    try:
        df = pd.read_excel(excel_file)

        required_columns = [
            'Назва',
            'Опис',
            'Вартість',
            'Тривалість'
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            request.session["import_result"] = {
                "summary": "У файлі відсутні необхідні колонки.",
                "total": 0,
                "imported": 0,
                "skipped": 0,
                "errors": [
                    f"Відсутні колонки: {', '.join(missing_columns)}"
                ],
            }
            return redirect("procedures-list")

        stats = {
            "total": len(df),
            "imported": 0,
            "skipped": 0,
            "errors": [],
        }

        for index, row in df.iterrows():
            excel_row = index + 2

            try:
                title = (
                    ""
                    if pd.isna(row["Назва"])
                    else str(row["Назва"]).strip()
                )

                description = (
                    ""
                    if pd.isna(row["Опис"])
                    else str(row["Опис"]).strip()
                )

                price = (
                    0.00
                    if pd.isna(row["Вартість"])
                    else float(row["Вартість"])
                )

                duration = (
                    0
                    if pd.isna(row["Тривалість"])
                    else int(row["Тривалість"])
                )

                # Обов'язкові поля
                missing_fields = []

                if not title:
                    missing_fields.append("Назва")

                if not price:
                    missing_fields.append("Вартість")

                if not duration:
                    missing_fields.append("Тривалість")

                if missing_fields:
                    stats["skipped"] += 1
                    stats["errors"].append(
                        f"Рядок {excel_row}: "
                        f"не заповнені поля: "
                        f"{', '.join(missing_fields)}."
                    )
                    continue

                if ProcedureModel.objects.filter(
                    title=title
                ).exists():
                    stats["skipped"] += 1
                    stats["errors"].append(
                        f"Рядок {excel_row}: "
                        f"Послуга з назвою '{title}' "
                        f"вже існує."
                    )
                    continue

                ProcedureModel.objects.create(
                    title=title,
                    description=description or None,
                    price=price,
                    duration=duration,
                )

                stats["imported"] += 1

            except Exception as exc:
                stats["skipped"] += 1
                stats["errors"].append(
                    f"Рядок {excel_row}: {exc}"
                )

        if stats["errors"]:
            if stats["imported"] > 0:
                message = (
                    f"Імпорт завершено з помилками. "
                    f"Додано {stats['imported']} "
                    f"з {stats['total']} клієнтів."
                )
            else:
                message = (
                    f"Імпорт не виконано. "
                    f"Жодного клієнта не додано "
                    f"з {stats['total']} записів."
                )
        else:
            message = (
                f"Імпорт завершено успішно. "
                f"Додано {stats['imported']} "
                f"з {stats['total']} послуг."
            )

        request.session["import_result"] = {
            "summary": message,
            "total": stats["total"],
            "imported": stats["imported"],
            "skipped": stats["skipped"],
            "errors": stats["errors"],
        }

        return redirect("procedures-list")

    except Exception as exc:
        request.session["import_result"] = {
            "summary": "Не вдалося обробити Excel-файл.",
            "total": 0,
            "imported": 0,
            "skipped": 0,
            "errors": [str(exc)],
        }

        return redirect("procedures-list")