from django.urls import path
from posts import views as posts_views


urlpatterns = [
    # path('', posts_views.show_posts, name='show_posts'),
    path('', posts_views.PostsShowView.as_view(), name='show_posts'),
    path('about/', posts_views.about, name='url_to_about'),
    # path('create', posts_views.create_post, name='create_post'),
    path('create', posts_views.PostCreateView.as_view(), name='create_post'),
    # path('update/<int:post_id>', posts_views.update_post, name='update'),
    path('update/<int:pk>', posts_views.PostUpdateView.as_view(), name='update'),
    path('<int:post_id>', posts_views.post, name='get_post'),
    path('delete/<int:post_id>', posts_views.delete, name='delete'),
    path('profile/<user_name>', posts_views.profile, name='profile'),
    # path('create/', posts_views.CreateView.as_view(), name='url_to_create_post'),
# FAKE
    path('fake/users', posts_views.fake_create_user),
    path('fake/posts', posts_views.fake_create_posts)
]