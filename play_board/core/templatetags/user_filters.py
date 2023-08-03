from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def addplaceholder(field, text):
    return field.as_widget(attrs={'placeholder': text})


@register.filter
def divide(value, arg):
    try:
        return int(value / arg * 100)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0
