from django.urls import reverse
from datetime import date, datetime
import pandas as pd
from django.core.paginator import Paginator
from django.db.models import Q, Case, When, IntegerField, Value
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from appointments.forms import AppointmentForm
from appointments.models import AppointmentModel

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
    client_created = request.GET.get("client_created") == "1"
    import_result = request.session.pop("import_result", None)

    paginator = Paginator(clients_qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "clients/list.html", {
        "clients": page_obj,
        "page_obj": page_obj,
        "clients_count": clients_count,
        "active_clients_count": active_clients_count,
        "client_created": client_created,
        "import_result": import_result,
    })

@login_required
def clients_detail_view(request, pk):
    client = get_object_or_404(ClientModel, pk=pk)
    appointments = AppointmentModel.objects.filter(
        client=client,
    ).exclude(
        status="canceled",
    ).annotate(
        status_order=Case(
            When(status="booked", then=Value(1)),
            When(status="done", then=Value(2)),
            output_field=IntegerField(),
        ),
    ).order_by(
        "status_order",
        "start_at",
    )[:5]

    age = None

    if client.birthdate:
        today = date.today()
        age = today.year - client.birthdate.year - (
            (today.month, today.day) < (client.birthdate.month, client.birthdate.day)
        )

    context = {
        "client": client,
        "appointments": appointments,
        "age": age
    }

    return render(request, "clients/detail.html", context)

@login_required
def client_create_view(request):
    if request.method == "POST":
        create_client_form = ClientForm(request.POST)

        if create_client_form.is_valid():
            create_client_form.save()
            create_client_form = ClientForm()
            response = HttpResponse()
            response["HX-Redirect"] = "/clients/?client_created=1"
            return response
    else:
        create_client_form = ClientForm()

    return render(request, "clients/partials/create_client_modal.html", {
        "create_client_form": create_client_form,
        "client_created": request.GET.get("client_created") == "1",
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

@login_required
def import_clients_view(request):
    if request.method != "POST":
        return render(
            request,
            "clients/partials/import_modal.html",
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
        return redirect("clients-list")

    try:
        df = pd.read_excel(excel_file)

        required_columns = [
            "Прізвище",
            "Імʼя",
            "Номер телефону",
            "Телеграм",
            "Стать",
            "Дата народження",
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
            return redirect("clients-list")

        stats = {
            "total": len(df),
            "imported": 0,
            "skipped": 0,
            "errors": [],
        }

        for index, row in df.iterrows():
            excel_row = index + 2

            try:
                last_name = (
                    ""
                    if pd.isna(row["Прізвище"])
                    else str(row["Прізвище"]).strip()
                )

                first_name = (
                    ""
                    if pd.isna(row["Імʼя"])
                    else str(row["Імʼя"]).strip()
                )

                phone_raw = (
                    ""
                    if pd.isna(row["Номер телефону"])
                    else str(row["Номер телефону"]).strip()
                )

                tg = (
                    ""
                    if pd.isna(row["Телеграм"])
                    else str(row["Телеграм"]).strip()
                )

                gender_raw = (
                    ""
                    if pd.isna(row["Стать"])
                    else str(row["Стать"]).strip().lower()
                )

                birthdate_raw = (
                    ""
                    if pd.isna(row["Дата народження"])
                    else str(row["Дата народження"]).strip()
                )

                # Обов'язкові поля
                missing_fields = []

                if not last_name:
                    missing_fields.append("Прізвище")

                if not first_name:
                    missing_fields.append("Імʼя")

                if not phone_raw:
                    missing_fields.append("Номер телефону")

                if missing_fields:
                    stats["skipped"] += 1
                    stats["errors"].append(
                        f"Рядок {excel_row}: "
                        f"не заповнені поля: "
                        f"{', '.join(missing_fields)}."
                    )
                    continue

                # Нормалізація телефону
                phone_number = phone_raw
                if len(phone_number) != 12:
                    stats["skipped"] += 1
                    stats["errors"].append(
                        f"Рядок {excel_row}: "
                        f"номер телефону '{phone_number}' "
                        f"має містити 12 знаків."
                    )
                    continue
                if phone_number.startswith("+"):
                    phone_number = phone_number[1:]

                phone_number = "+" + phone_number

                # Перевірка телефону
                if ClientModel.objects.filter(
                    phone_number=phone_number
                ).exists():
                    stats["skipped"] += 1
                    stats["errors"].append(
                        f"Рядок {excel_row}: "
                        f"номер телефону '{phone_number}' "
                        f"вже існує."
                    )
                    continue

                # Telegram необов'язковий
                if tg and ClientModel.objects.filter(tg=tg).exists():
                    stats["skipped"] += 1
                    stats["errors"].append(
                        f"Рядок {excel_row}: "
                        f"Telegram '@{tg}' вже існує."
                    )
                    continue

                if tg.startswith("@"):
                    stats["skipped"] += 1
                    stats["errors"].append(
                        f"Рядок {excel_row}: "
                        f"Telegram '{tg}' не має починатись з '@'"
                    )
                    continue

                # Стать
                gender = None

                if gender_raw:
                    gender_map = {
                        "чоловік": "male",
                        "жінка": "female",
                    }

                    gender = gender_map.get(gender_raw.lower())

                    if gender is None:
                        stats["skipped"] += 1
                        stats["errors"].append(
                            f"Рядок {excel_row}: "
                            f"некоректне значення статі "
                            f"'{gender_raw}'."
                        )
                        continue

                # Дата народження необов'язкова
                birthdate = None

                if birthdate_raw:
                    try:
                        birthdate = datetime.strptime(
                            birthdate_raw,
                            "%d.%m.%Y",
                        ).date()

                    except ValueError:
                        stats["skipped"] += 1
                        stats["errors"].append(
                            f"Рядок {excel_row}: "
                            f"некоректна дата народження "
                            f"'{birthdate_raw}'. "
                            f"Очікується ДД.ММ.РРРР."
                        )
                        continue

                ClientModel.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    tg=tg or None,
                    gender=gender,
                    birthdate=birthdate,
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
                f"з {stats['total']} клієнтів."
            )

        request.session["import_result"] = {
            "summary": message,
            "total": stats["total"],
            "imported": stats["imported"],
            "skipped": stats["skipped"],
            "errors": stats["errors"],
        }

        return redirect("clients-list")

    except Exception as exc:
        request.session["import_result"] = {
            "summary": "Не вдалося обробити Excel-файл.",
            "total": 0,
            "imported": 0,
            "skipped": 0,
            "errors": [str(exc)],
        }

        return redirect("clients-list")

@login_required
def client_appointment_create(request, pk):
    client = get_object_or_404(ClientModel, pk=pk)

    if request.method == "POST":
        create_appointment_form = AppointmentForm(
            request.POST,
            client=client
        )

        if create_appointment_form.is_valid():
            appointment = create_appointment_form.save(commit=False)
            appointment.client = client
            appointment.save()

            response = HttpResponse(status=200)
            response["HX-Redirect"] = reverse(
                "clients-detail",
                kwargs={"pk": client.pk},
            )

            return response

    else:
        create_appointment_form = AppointmentForm(client=client)

    return render(
        request,
        "appointments/partials/create_modal.html",
        {
            "create_appointment_form": create_appointment_form,
            "form_action": reverse(
            "client-appointment-create",
            kwargs={"pk": client.pk}),
        },
    )