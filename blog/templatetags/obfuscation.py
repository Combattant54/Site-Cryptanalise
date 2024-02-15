from django import template


register = template.Library()

@register.filter(is_safe=True)
def obfuscate_mail(mail_address):
    private, extension = mail_address.split("@")
    return private[0] + "*" * 6 + private[-1] + "@" + extension