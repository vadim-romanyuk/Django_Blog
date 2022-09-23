from django.contrib import admin
from .models import Post, Profile, Log
# Register your models here.

# admin.site.register(Post)


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'user', 'user_phone')
    ordering = ('-date',)
    search_fields = ('title', 'date',)

    list_filter = ('user',)

    @admin.display(description='phone nomber')
    def user_phone(self, odj: Post):
        return Profile.objects.get(user_id=obj.user.id).phone
