from django import template

register = template.Library()
@register.filter(is_safe=True)
def field_join(objects, attr_name, separator=", "):
    return separator.join(getattr(i, attr_name) for i in objects)