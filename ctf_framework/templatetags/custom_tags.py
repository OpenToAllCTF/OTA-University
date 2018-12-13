from django import template

register = template.Library()

def kebab(value):
    """Replaces spaces with dashes."""
    return value.replace(' ', '-')

register.filter('kebab', kebab)

