from django import template

from webapp.models import ReadPost, Category

register = template.Library()


@register.inclusion_tag('top_category_post.html')
def get_category_top():
    categories = Category.objects.all()
    posts = list()
    for category in categories:
        posts.append(
            ReadPost.objects.filter(status='published').filter(category__name=category).order_by('views').first()
        )
    return {'most_pop_cat_posts': posts}
