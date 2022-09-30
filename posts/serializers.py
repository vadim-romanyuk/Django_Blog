from rest_framework import serializers, permissions
from .models import Post
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """для вывода"""
    phone = serializers.CharField(source='profile.phone', max_length=20, required=False)
    address = serializers.CharField(source='profile.phone', max_length=500, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'address')


class UserCreateSerializer(UserSerializer):
    """для создания"""

    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'address', 'password')

class PostSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=100)
    content = serializers.CharField(required=True)

    def update(self, instance: Post, validated_data):
        instance.title = validated_data['title']
        instance.content = validated_data['content']
        instance.save()
        return instance

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class PostsModelSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)

    class Meta:
        model = Post
        fields = ('title', 'content', 'date', 'user', 'id')
        read_only_fields = ('date',)








class PostPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, post: Post):
        if request.method in permissions.SAFE_METHODS:
            return True
        post_permission = post.user == request.user
        print(request.user, f'{post_permission}')
        return post_permission


