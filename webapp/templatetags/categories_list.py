from django import template

from webapp.models import Category

register = template.Library()


@register.inclusion_tag('categories.html')
def get_list_categories():
    return {'categories': Category.objects.all().order_by('-pk')}
