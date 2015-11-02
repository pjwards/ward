from .models import User, Group, Post, Comment, Media, Attachment
from rest_framework import serializers

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = '__all__'


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = '__all__'
        depth = 1


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = '__all__'
        depth = 1


class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
        read_only_fields = '__all__'


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'
        read_only_fields = '__all__'
        depth = 1
