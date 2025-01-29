from django import template
from movies.models import Category

register = template.Library() # для регистрации наших тегов (в django)

@register.simple_tag() # этот декоратор позволит зарегать наш тег (в django)
def get_categories():
    return Category.objects.all()