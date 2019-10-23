from django.contrib import admin
from django.conf import settings
# from django.conf.urls import path, handler404, handler500
from django.conf.urls.static import static

from django.urls import path

from webapp import views


# handler404 = views.handler404
# handler500 = views.handler500

urlpatterns = [
    path('search/', views.search, name='search'),\
    path('about/', views.about, name='about'),
    # path('404/$', views.handler404, name='handler404'),
    # path('500/$', views.handler500, name='handler500'),
]

urlpatterns += [
    path('', views.HomePage.as_view(), name="home"),
    path('new_posts/', views.NewPosts.as_view(), name="latest-posts"),
    path('popular/', views.PopularPosts.as_view(), name="popular-posts"),
    path('category/<int:pk>/', views.CategoryPosts.as_view(), name='category'),
    path('view/<int:pk>/', views.ViewPost.as_view(), name='view_post'),
    path('tag/<int:pk>/', views.TagPosts.as_view(), name='tag'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
