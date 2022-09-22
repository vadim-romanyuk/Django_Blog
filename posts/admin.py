from django.contrib import admin
from .models import Post, Profile, Log
# Register your models here.

# admin.site.register(Post)


@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'user')
    ordering = ('-date',)
