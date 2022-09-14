from django.urls import path
from posts import views as posts_views


urlpatterns = {
    path('', posts_views.show_posts),
    path('about/', posts_views.about, name='url_to_about'),
    path('create', posts_views.create_post, name='create_post'),
    path('update/<int:post_id>', posts_views.update_post, name='update'),
    path('<int:post_id>', posts_views.post, name='get_post'),
    path('delete/<int:post_id>', posts_views.delete, name='delete'),
    path('profile/<int:user_name>', posts_views.profile, name='profile')
    # path('create/', posts_views.CreateView.as_view(), name='url_to_create_post'),
    # FAKE
    #     path('fake/users', posts_views.fake_create_user),
    #     path('fake/posts', posts_views.fake_create_posts)
}