document.addEventListener('DOMContentLoaded', function () {

    const calendarEl = document.getElementById('calendar');
    const masterSelect = document.getElementById('masterSelect');
    const eventModalEl = document.getElementById('eventModal');
    const createAppointmentModalEl = document.getElementById('createAppointmentModal');
    const updateAppointmentModalEl = document.getElementById('updateAppointmentModal');
    const deleteAppointmentModalEl = document.getElementById('deleteAppointmentModal');
    const editBtn = document.getElementById('eventEditBtn');
    const deleteBtn = document.getElementById('eventDeleteBtn');

    let selectedMaster = '';
    let currentEventId = null;

    const STATUS_CONFIG = {
        booked: { icon: 'bi-bookmark-check-fill' },
        done: { icon: 'bi-check-circle-fill' },
        canceled: { icon: 'bi-x-circle-fill' },
        no_show: { icon: 'bi-eye-slash-fill' },
    };

    const calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'uk',
        timeZone: 'local',
        buttonText: {
            today: 'Сьогодні',
            month: 'Місяць',
            week: 'Тиждень',
            day: 'День',
            list: 'Список',
        },
        
        initialDate: new Date(),
        firstDay: 1,
        weekends: true,

        nowIndicator: true,
        navLinks: true,

        selectable: true,
        selectMirror: true,

        editable: true,
        eventResizableFromStart: true,

        dayMaxEvents: true,
        expandRows: true,

        initialView: 'timeGridWeek',
        height: 'auto',

        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek',
        },

        slotMinTime: '08:00:00',
        slotMaxTime: '22:00:00',
        slotDuration: '00:10:00',
        slotLabelInterval: '01:00',
        slotLabelFormat: {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false,
        },

        businessHours: {
            daysOfWeek: [0, 1, 2, 3, 4, 5, 6], // Пн-Нд
            startTime: '08:00',
            endTime: '20:00',
        },
        snapDuration: '00:10:00',
        selectConstraint: "businessHours",
        eventConstraint: "businessHours",
        displayEventEnd: true,
        // eventBackgroundColor: '#198754',
        // eventBorderColor: '#198754',
        // eventTextColor: '#fff',
        allDaySlot: false,

        events(fetchInfo, success, failure) {
            const params = new URLSearchParams({
                start: fetchInfo.startStr,
                end: fetchInfo.endStr,
            });

            if (selectedMaster) {
                params.set('master', selectedMaster);
            }

            fetch(`/appointments/api/?${params.toString()}`)
                .then((r) => r.json())
                .then(success)
                .catch(failure);
        },

        eventClick(info) {
            const event = info.event;
            const props = event.extendedProps;

            currentEventId = event.id;

            document.getElementById('eventTitle').innerText = `Інформація про запис #${event.id}`;

            document.getElementById('eventProcedureTitle').innerHTML =
                `${props.clientName} <strong>${formatDateTime(event.start)}</strong>`;

            document.getElementById('eventClient').innerText =
                props.clientName || '-';

            document.getElementById('eventMaster').innerText =
                props.masterName || '-';

            document.getElementById('eventProcedure').innerText =
                props.procedureName || '-';

            document.getElementById('eventStart').innerText =
                formatDateTime(event.start) || event.start;

            document.getElementById('eventEnd').innerText =
                formatDateTime(event.end) || event.end;

            document.getElementById('eventDuration').innerText =
                props.procedureDuration
                    ? `${props.procedureDuration} хв`
                    : '-';

            document.getElementById('eventPrice').innerText =
                formatPrice(props.procedurePrice);

            setStatusBadge(
                document.getElementById('eventStatus'),
                props.statusKey,
                props.status
            );

            document.getElementById('eventComment').innerText =
                props.comment || '-';

            bootstrap.Modal.getOrCreateInstance(eventModalEl).show();
        },

        eventContent(arg) {
            const event = arg.event;

            const wrapper = document.createElement('div');
            wrapper.style.padding = '4px';
            wrapper.style.borderRadius = '6px';
            wrapper.style.fontSize = '12px';
            wrapper.style.lineHeight = '1.2';
            wrapper.style.overflow = 'hidden';

            const title = document.createElement('div');
            title.innerText = event.title;
            title.style.fontWeight = '600';
            title.style.fontSize = '13px';

            const master = document.createElement('div');
            master.innerText = event.extendedProps.masterName || '';
            master.style.fontSize = '11px';
            master.style.opacity = '0.75';

            const procedure = document.createElement('div');
            procedure.innerText = event.extendedProps.procedureName || '';
            procedure.style.fontSize = '11px';
            procedure.style.opacity = '0.75';

            wrapper.appendChild(title);
            wrapper.appendChild(master);
            wrapper.appendChild(procedure);

            return { domNodes: [wrapper] };
        },
        eventDataTransform(event) {
            if (event.extendedProps.statusKey === "done") {
                event.color = "#11766e"; // сірий
            } else {
                event.color = event.color;
            }
        
            return event;
        },
    });

    function formatDateTime(date) {
        if (!date) return '-';
    
        return `${date.toLocaleDateString('uk-UA')} ${date.toLocaleTimeString('uk-UA', {
            hour: '2-digit',
            minute: '2-digit',
        })}`;
    }

    function formatPrice(value) {
        if (value === null || value === undefined || value === '') return '-';
        return `${Number(value).toLocaleString('uk-UA', {
            minimumFractionDigits: 0,
            maximumFractionDigits: 2,
        })} ₴`;
    }

    function setStatusBadge(el, statusKey, statusLabel) {
        const config = STATUS_CONFIG[statusKey] || { icon: 'bi-info-circle-fill' };
        el.className = `appointment-status-badge status-${statusKey || 'booked'}`;
        el.innerHTML = `<i class="bi ${config.icon}"></i><span>${statusLabel || '-'}</span>`;
    }

    function openSecondaryModal(modalEl, targetId, url) {
        bootstrap.Modal.getInstance(eventModalEl)?.hide();

        htmx.ajax('GET', url, {
            target: targetId,
            swap: 'innerHTML',
        }).then(() => {
            bootstrap.Modal.getOrCreateInstance(modalEl).show();
        });
    }

    editBtn.addEventListener('click', () => {
        if (!currentEventId) return;
        openSecondaryModal(
            updateAppointmentModalEl,
            '#updateAppointmentModalBody',
            `/appointments/update/${currentEventId}/`
        );
    });

    deleteBtn.addEventListener('click', () => {
        if (!currentEventId) return;
        openSecondaryModal(
            deleteAppointmentModalEl,
            '#deleteAppointmentModalBody',
            `/appointments/delete/${currentEventId}/`
        );
    });

    calendar.render();

    masterSelect.addEventListener('change', function () {
        selectedMaster = this.value;
        calendar.refetchEvents();
    });

    document.body.addEventListener('appointment-updated', () => {
        bootstrap.Modal.getInstance(updateAppointmentModalEl)?.hide();
        calendar.refetchEvents();
    });

    document.body.addEventListener('appointment-deleted', () => {
        bootstrap.Modal.getInstance(deleteAppointmentModalEl)?.hide();
        calendar.refetchEvents();
    });
    document.body.addEventListener('appointment-created', () => {
        bootstrap.Modal.getInstance(createAppointmentModalEl)?.hide();
        calendar.refetchEvents();
    });

});
