from django.contrib import admin
from django.conf import settings
# from django.conf.urls import path, handler404, handler500
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from webapp import views
from webapp.sitemaps import PostSitemap, TagSitemap, CategorySitemap


# handler404 = 'webapp.views.handler404'
# handler500 = 'webapp.views.handler500'

sitemaps = {
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'tags': TagSitemap
}

urlpatterns = [
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    # path('404/', views.handler404, name='handler404'),
    # path('500/', views.handler500, name='handler500'),
]

urlpatterns += [
    # path('api/v1/user/', views.UserProfile.as_view(), name='user_profile'),
    path('api/v1/user_profile/', views.UserProfileRest.as_view(), name='user-profile-rest'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]

urlpatterns += [
    path('', views.HomePage.as_view(), name="home"),
    path('new_posts/', views.NewPosts.as_view(), name="latest-posts"),
    path('popular/', views.PopularPosts.as_view(), name="popular-posts"),
    # path('category/<int:pk>/', views.CategoryPosts.as_view(), name='category'),
    # path('view/<int:pk>/', views.ViewPost.as_view(), name='view_post'),

    path('article/<slug>/', views.ViewPost.as_view(), name='view_post_slug'),
    path('category/<slug>/', views.CategoryPosts.as_view(), name='category_slug'),
    path('tag/<slug>/', views.TagPosts.as_view(), name='tag_slug'),

    # path('tag/<int:pk>/', views.TagPosts.as_view(), name='tag'),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
