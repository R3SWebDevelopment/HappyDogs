import json
from django import template
register = template.Library()

@register.simple_tag
def ng_output(id = None):
    if id is not None:
        return "{{ %s }}" % id
    return ""