import random

from django.core.management.base import BaseCommand, CommandError

from datacenter.management.utils import get_pupil
from datacenter.models import Commendation, Lesson, Subject

COMMENDATIONS = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Очень хороший ответ!",
    "Ты сегодня прыгнул выше головы!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Замечательно!",
    "Так держать!",
    "Ты на верном пути!",
    "Здорово!",
]


class Command(BaseCommand):
    help = "Хвалит ученика"

    def add_arguments(self, parser):
        parser.add_argument("full_name", nargs=1, help="Фамилия и имя ученика")
        parser.add_argument("subject", nargs="+", help="Учебный предмет")

    def handle(self, *args, **options):
        pupil, name = get_pupil(**options)
        subject = " ".join(options["subject"]).capitalize()
        try:
            lesson = Lesson.objects.filter(
                year_of_study=pupil.year_of_study,
                group_letter=pupil.group_letter,
                subject__title__contains=subject,
            ).order_by("-date")[0]
        except IndexError:
            raise CommandError(f"{subject} нет в списке предметов")

        Commendation.objects.create(
            text=random.choice(COMMENDATIONS),
            created=lesson.date,
            schoolkid=pupil,
            subject=lesson.subject,
            teacher=lesson.teacher,
        )

        self.stdout.write(self.style.SUCCESS(f"Похвала ученику {name} добавлена"))
