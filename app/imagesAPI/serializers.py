from rest_framework import serializers

from .models import Image, Comment


class ImageSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Comment.objects.all(),
    )

    class Meta:
        model = Image
        fields = ('id', 'title', 'imagefile', 'comments')
        read_only_fields = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    image_title = serializers.ReadOnlyField(source='image_post.title')

    class Meta:
        model = Comment
        fields = ('id', 'name', 'body', 'image_post', 'image_title')
        read_only_fields = ('id', 'image_title')


class CommentUpdateSerializer(serializers.ModelSerializer):
    image_title = serializers.ReadOnlyField(source='image_post.title')

    class Meta:
        model = Comment
        fields = ('id', 'name', 'body', 'image_post', 'image_title')
        read_only_fields = ('id', 'name', 'image_post', 'image_title')
