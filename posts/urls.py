from django.urls import path
from posts import views as posts_views


urlpatterns = [
    path('about/', posts_views.about, name='url_to_about'),
    # path('create', posts_views.create_post, name='create_post'),
    path('<str:post_id>', posts_views.posts),
    path('create/', posts_views.create_post, name='url_to_create_post'),
]