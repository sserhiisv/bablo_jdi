from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, handler404, handler500
from django.conf.urls.static import static

from webapp import views


# handler404 = views.handler404
# handler500 = views.handler500

urlpatterns = [
    ######
    url(r'^search/$', views.search, name='search'),
    ######
    url(r'^about/$', views.about, name='about'),
    # url(r'^404/$', views.handler404, name='handler404'),
    # url(r'^500/$', views.handler500, name='handler500'),
]

urlpatterns += [
    url(r'^$', views.HomePage.as_view(), name="home"),
    url(r'^new_posts/$', views.NewPosts.as_view(), name="latest-posts"),
    url(r'^popular/$', views.PopularPosts.as_view(), name="popular-posts"),
    url(r'^category/(?P<pk>\d+)/$', views.CategoryPosts.as_view(), name='category'),
    url(r'^view/(?P<pk>\d+)/$', views.ViewPost.as_view(), name='view_post'),
    url(r'^tag/(?P<pk>\d+)/$', views.TagPosts.as_view(), name='tag'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
