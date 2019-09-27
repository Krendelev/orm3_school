from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.management.base import BaseCommand, CommandError
from datacenter.models import Schoolkid


def get_pupil(**options):
    name = " ".join(name.capitalize() for name in options["full_name"][0].split())
    try:
        pupil = Schoolkid.objects.get(full_name__contains=name)
    except ObjectDoesNotExist:
        raise CommandError(f"Ученик {name} не найден")
    except MultipleObjectsReturned:
        raise CommandError(
            f"Найдено несколько учеников с именем {name}. Уточните запрос"
        )
    return pupil
