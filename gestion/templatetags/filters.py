from django import template

register = template.Library()

@register.filter
def state_css_class(value):
    """returns appropriate bootstrap label class for states"""
    statemap = {
        4: 'badge-success',
        1: 'badge-warning',
    }
    try:
        return statemap[value]
    except KeyError:
        return 'badge-warning'