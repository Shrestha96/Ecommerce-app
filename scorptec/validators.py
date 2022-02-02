from django.core.exceptions import ValidationError
from django.utils import timezone


def get_today():
    return timezone.now().astimezone().date()


def validate_dob(value):
    year_diff = get_today().year - value.year
    if year_diff <= 16:
        raise ValidationError('You must be above 16 years to register.')
    return value
