from urllib.parse import quote_plus
from django import template

register  = template.Library()

@register.filter  #django template library registered as filter
def urlify(value):
	return quote_plus(value)
