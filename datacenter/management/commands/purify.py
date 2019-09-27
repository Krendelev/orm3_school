from django.core.management.base import BaseCommand, CommandError

from datacenter.management.utils import get_pupil
from datacenter.models import Chastisement


class Command(BaseCommand):
    help = "Удаляет замечания ученику"

    def add_arguments(self, parser):
        parser.add_argument("full_name", nargs="+", help="Фамилия и имя ученика")

    def handle(self, *args, **options):
        pupil, name = get_pupil(**options)
        Chastisement.objects.filter(schoolkid=pupil).delete()

        self.stdout.write(self.style.SUCCESS(f"Замечания ученику {name} удалены"))
