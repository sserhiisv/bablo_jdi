from django import template

from webapp.models import ReadPost

register = template.Library()


@register.inclusion_tag('random_advice.html')
def get_random_advice():
    return {'random_advice_posts': ReadPost.objects.filter(status='published').order_by('?')[:4]}
