from archive.models import User, Group, Post, Comment, Media, Attachment
from rest_framework import serializers

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comment-detail')
    posts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='post-detail')

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = '__all__'


class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
        read_only_fields = '__all__'


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attachment
        # fields = '__all__'
        exclude = ('post', 'comment')
        read_only_fields = '__all__'
        depth = 1


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comment-detail')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = '__all__'
        depth = 1


class PostSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    # attachments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='attachment-detail')
    comments = serializers.HyperlinkedIdentityField(many=True, read_only=True, view_name='comment-detail')
    # comments = CommentSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = '__all__'
        depth = 1
