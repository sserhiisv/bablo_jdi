from django import template

from webapp.models import ReadPost, Category

register = template.Library()


@register.inclusion_tag('top_category_post.html', takes_context=True)
def get_category_top(context):
    categories = Category.objects.all()
    posts = []
    for category in categories:
        posts.append(
            ReadPost.objects.filter(status='published').filter(category__name=category).order_by('views').first()
        )
    if not posts:
        posts.append(ReadPost.objects.first())
    context['most_pop_cat_posts'] = ReadPost.objects.all()
    return context
