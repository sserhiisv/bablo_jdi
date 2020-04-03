from __future__ import unicode_literals

import sorl

from django.contrib.auth.models import User

from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation

from uuslug import uuslug
from ckeditor.fields import RichTextField
from hitcount.models import HitCount, HitCountMixin


STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('withdrawn', 'Withdrawn'),
)


class Category(models.Model):
    name = models.CharField('Name', max_length=100)
    name_ua = models.CharField('Name_ua', max_length=100, default='')
    slug = models.SlugField('Slug')
    icon = models.CharField('Icon', max_length=50, default='')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = uuslug(self.name, instance=self)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'category',
            kwargs={
                'pk': self.pk
            }
        )


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField('Slug', default='')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = uuslug(self.title, instance=self)
        super(Tag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'tag',
            kwargs={
                'pk': self.pk
            }
        )


class ReadPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = RichTextField(config_name='ckeditor')
    content = RichTextField(config_name='ckeditor')
    date = models.DateTimeField()
    image = sorl.thumbnail.ImageField(null=False, blank=False, upload_to='images/posts', verbose_name=u'Images')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='draft')
    slug = models.SlugField('Slug')
    tag = models.ManyToManyField(Tag, related_name='readposts')
    views = GenericRelation(HitCount,
                            object_id_field='object_pk',
                            related_query_name='hit_count_generic_relation')

    class Meta:
        verbose_name = 'ReadPost'
        verbose_name_plural = 'ReadPosts'
        ordering = ("-date",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = uuslug(self.title, instance=self)
        super(ReadPost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'view_post',
            kwargs={
                'pk': self.pk
            }
        )


class Profile(models.Model):
    username = models.CharField(default='AppUser', max_length=256)
    score = models.IntegerField(default=0)
    friend_score = models.IntegerField(default=0)
    money_output = models.FloatField(default=0)
    android_id = models.CharField(default='', max_length=256, unique=True)
    referal_id = models.CharField(default='', max_length=256, unique=True)
    timestamp = models.CharField(default='', max_length=256)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f'android #{self.android_id} profile'


class Referal(models.Model):
    referal_id = models.CharField(default='', max_length=256)
    android_id_from = models.CharField(default='', max_length=256)
    android_id_to = models.CharField(default='', max_length=256)

    def __str__(self):
        return f'referal #{self.referal_id} profile'
