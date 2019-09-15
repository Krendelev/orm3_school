from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from datacenter.models import Commendation
from datacenter.models import Lesson
from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Subject
from datacenter.models import Chastisement


class Command(BaseCommand):
    help = "Удаляет замечания ученику"

    def add_arguments(self, parser):
        parser.add_argument("full_name", nargs=2, help="Имя и фамилия ученика")

    def handle(self, *args, **options):
        name1, name2 = [name.capitalize() for name in options["full_name"]]
        try:
            pupil = Schoolkid.objects.filter(
                Q(full_name__contains=name1) & Q(full_name__contains=name2)
            )[0]
        except IndexError:
            raise CommandError(f"Ученик {name1} {name2} не найден")

        Chastisement.objects.filter(schoolkid=pupil).delete()

        self.stdout.write(
            self.style.SUCCESS(f"Замечания ученику {name1} {name2} удалены")
        )
