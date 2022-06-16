from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            ('%(value)s - неверное значение! Текущий год {current_year}'),
            params={'value': value},
        )
