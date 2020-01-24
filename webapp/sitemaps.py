from django.contrib.sitemaps import Sitemap
from .models import ReadPost, Category, Tag


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return ReadPost.objects.all()

    def lastmod(self, obj):
        return obj.date


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Category.objects.all()

    # def lastmod(self, obj):
    #     return obj.date


class TagSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Tag.objects.all()

    # def lastmod(self, obj):
    #     return obj.date
