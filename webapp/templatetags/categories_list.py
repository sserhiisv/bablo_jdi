from django import template

from webapp.models import Category

register = template.Library()


@register.inclusion_tag('categories.html', takes_context=True)
def get_list_categories(context):
    context['categories'] = Category.objects.all().order_by('-pk')
    return context
