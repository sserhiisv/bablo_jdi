from django import template

from webapp.models import ReadPost

register = template.Library()


@register.inclusion_tag('most_reading_posts.html', takes_context=True)
def get_most_reading(context):
    context['most_read_posts'] = ReadPost.objects.filter(status='published').order_by('views')[:2]
    return context
