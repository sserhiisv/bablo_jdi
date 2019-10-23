from django import template

from webapp.models import ReadPost

register = template.Library()


@register.inclusion_tag('random_advice.html', takes_context=True)
def get_random_advice(context):
    context['random_advice_posts'] = ReadPost.objects.filter(status='published').order_by('?')[:4]
    return context
