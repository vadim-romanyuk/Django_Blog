from rest_framework import serializers
from .models import Post


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
    user = serializers.RelatedField(source='user.username')

    class Meta:
        model = Post
        fields = ['title', 'content', 'date', 'user']
        read_only_fields = ('date',)
