from django.core.management.base import BaseCommand, CommandError

from datacenter.management.utils import get_pupil
from datacenter.models import Mark


class Command(BaseCommand):
    help = "Исправляет плохие оценки на хорошие"

    def add_arguments(self, parser):
        parser.add_argument("full_name", nargs="+", help="Фамилия и имя ученика")

    def handle(self, *args, **options):
        pupil = get_pupil(**options)
        bad_marks = Mark.objects.filter(schoolkid=pupil, points__lte=3)
        bad_marks.update(points=5)

        self.stdout.write(
            self.style.SUCCESS(f"Оценки ученика {pupil.full_name} исправлены")
        )
