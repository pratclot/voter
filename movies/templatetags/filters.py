from django.template.library import Library

register = Library()


@register.filter(name='dj_getattr')
def dj_getattr(value, arg):
    return getattr(value, str(arg))
