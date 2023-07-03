from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.-@]+\Z'
    message = 'Введите имя пользователя: буквы, цифры, @, _ или -'
    flags = 0


username_validator = UnicodeUsernameValidator()
