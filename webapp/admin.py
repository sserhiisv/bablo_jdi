from django.contrib import admin
from django.utils.html import format_html

from sorl.thumbnail import get_thumbnail

from webapp.models import ReadPost, Category, Tag


@admin.register(ReadPost)
class PostAdmin(admin.ModelAdmin):
    fields = ['id', 'title', 'author', 'tag', 'category', 'description', 'content', 'date', 'image']
    list_display = ['id', 'title', 'photo_thumbnail', 'slug', 'status', 'category', 'date']
    list_filter = ['id', 'date', 'title', 'category', 'status']
    search_fields = ['id', 'title', 'status', 'date', 'category', 'author']
    actions = ['make_published', 'make_draft', 'make_withdrawn']

    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='published')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
            self.message_user(request, "%s successfully marked as published." % message_bit)

    def make_draft(self, request, queryset):
        rows_updated = queryset.update(status='draft')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
            self.message_user(request, "%s successfully marked as draft." % message_bit)

    def make_withdrawn(self, request, queryset):
        rows_updated = queryset.update(status='withdrawn')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
            self.message_user(request, "%s successfully marked as withdrawn." % message_bit)

    def photo_thumbnail(self, obj):
        im = get_thumbnail(obj.image, '60x60', quality=99)
        return format_html(
            '<img src="{}" border="0" alt="" width="{}" height="{}" />',
            im.url, im.width, im.height
        )

    photo_thumbnail.short_description = u'Foto'
    photo_thumbnail.allow_tags = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'name_ua', 'icon']
    list_display = ['name', 'name_ua', 'slug']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ['title']
    list_display = ['title', 'slug']
