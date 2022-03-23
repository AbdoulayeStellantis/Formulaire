from django import template
from django.contrib.auth.models import Group
import pprint

register = template.Library()

@register.filter
def is_member(user, group_name): 	
	try:
		group = Group.objects.get(name=group_name) 
	except:
		group = None
	return True if group in user.groups.all() else False
    