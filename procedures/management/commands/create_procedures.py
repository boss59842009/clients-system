from django.core.management.base import BaseCommand

from procedures.models import ProcedureModel


class Command(BaseCommand):
    help = "Створення тестових процедур"

    def handle(self, *args, **kwargs):
        procedures = [
            ProcedureModel(
                title="Загальнооздоровчий масаж (спина, шия, голова, руки, ноги, живіт, стопи)",
                description="",
                price=800,
                duration=60,
                is_active=True,
            ),
            ProcedureModel(
                title="Загальнооздоровчий масаж (спина, шия, голова, руки, ноги, живіт, стопи)",
                description="",
                price=950,
                duration=90,
                is_active=True,
            ),
            ProcedureModel(
                title="Масаж спини, шиї, голови та рук",
                description="",
                price=500,
                duration=45,
                is_active=True,
            ),
            ProcedureModel(
                title="Масаж спини, шиї, голови та рук",
                description="",
                price=650,
                duration=60,
                is_active=True,
            ),
            ProcedureModel(
                title="Лімфодренажний масаж (все тіло)",
                description="",
                price=850,
                duration=60,
                is_active=True,
            ),
            ProcedureModel(
                title="Вісцеральний масаж + альгінатна маска",
                description="",
                price=600,
                duration=45,
                is_active=True,
            ),
            ProcedureModel(
                title="Стоун-терапія",
                description="",
                price=900,
                duration=90,
                is_active=True,
            ),
            ProcedureModel(
                title="Моделюючий масаж (антицелюлітний + масаж шиї та рук)",
                description="",
                price=850,
                duration=60,
                is_active=True,
            ),
            ProcedureModel(
                title="Моделюючий масаж (антицелюлітний + масаж шиї та рук)",
                description="",
                price=1000,
                duration=90,
                is_active=True,
            ),
            ProcedureModel(
                title="Антицелюлітний масаж (живіт, боки, сідниці, ноги)",
                description="",
                price=750,
                duration=45,
                is_active=True,
            ),
            ProcedureModel(
                title="Антицелюлітний масаж (живіт, боки, сідниці, ноги)",
                description="",
                price=900,
                duration=60,
                is_active=True,
            ),
            ProcedureModel(
                title="Медовий моделюючий масаж",
                description="",
                price=900,
                duration=60,
                is_active=True,
            ),
            ProcedureModel(
                title="Антицелюлітне обгортання",
                description="",
                price=850,
                duration=60,
                is_active=True,
            ),
            ProcedureModel(
                title="Антицелюлітне обгортання",
                description="",
                price=1000,
                duration=90,
                is_active=True,
            ),
            ProcedureModel(
                title="Бандажне обгортання (скрабування + закріплення коригуючим кремом)",
                description="",
                price=900,
                duration=90,
                is_active=True,
            ),
            ProcedureModel(
                title="Релакс-масаж «Баунті» (ноги + сідниці)",
                description="",
                price=750,
                duration=60,
                is_active=True,
            ),
            ProcedureModel(
                title="Пресотерапія",
                description="",
                price=450,
                duration=30,
                is_active=True,
            ),
            ProcedureModel(
                title="Пресотерапія",
                description="",
                price=650,
                duration=60,
                is_active=True,
            ),
            ProcedureModel(
                title="Ендосфера (все тіло)",
                description="",
                price=750,
                duration=45,
                is_active=True,
            ),
            ProcedureModel(
                title="Ендосфера (все тіло)",
                description="",
                price=900,
                duration=60,
                is_active=True,
            ),
            ProcedureModel(
                title="Ендосфера (живіт + ноги)",
                description="",
                price=600,
                duration=45,
                is_active=True,
            ),
            ProcedureModel(
                title="Ендосфера (живіт + ноги)",
                description="",
                price=700,
                duration=60,
                is_active=True,
            ),
            ProcedureModel(
                title="Кавітація (1 зона) + вакуумний масаж",
                description="",
                price=550,
                duration=50,
                is_active=True,
            ),
            ProcedureModel(
                title="Кавітація (1 зона) + RF-ліфтинг (1 зона) + вакуумний масаж",
                description="",
                price=600,
                duration=60,
                is_active=True,
            ),
            ProcedureModel(
                title="Вакуумний масаж (все тіло) + RF-ліфтинг (1 зона)",
                description="",
                price=800,
                duration=90,
                is_active=True,
            ),
            ProcedureModel(
                title="Міостимуляція (1 зона)",
                description="",
                price=400,
                duration=30,
                is_active=True,
            ),
            ProcedureModel(
                title="Масаж обличчя, шиї та декольте",
                description="",
                price=550,
                duration=45,
                is_active=True,
            ),
            ProcedureModel(
                title="Масаж у чотири руки",
                description="",
                price=0,
                duration=60,
                is_active=True,
            ),
            ProcedureModel(
                title="Масаж у чотири руки",
                description="",
                price=0,
                duration=90,
                is_active=True,
            ),
            ProcedureModel(
                title="Міофасціальний масаж обличчя",
                description="",
                price=650,
                duration=0,
                is_active=True,
            ),
            ProcedureModel(
                title="Букальний масаж обличчя",
                description="",
                price=700,
                duration=0,
                is_active=True,
            ),
        ]

        created = ProcedureModel.objects.bulk_create(
            procedures,
            ignore_conflicts=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Створено {len(created)} процедур"
            )
        )