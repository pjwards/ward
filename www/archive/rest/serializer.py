from archive.models import *
from rest_framework import serializers


# Serializers define the API representation.
class FBUserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for facebook user
    """
    id = serializers.ReadOnlyField()
    # comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comment-detail')
    # posts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='post-detail')

    class Meta:
        model = FBUser
        exclude = ('groups',)
        read_only_fields = '__all__'


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for facebook group
    """
    id = serializers.ReadOnlyField()
    owner = FBUserSerializer(read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = '__all__'


class MediaSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for facebook media
    """
    class Meta:
        model = Media
        fields = '__all__'
        read_only_fields = '__all__'


class AttachmentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for facebook attachment
    """
    class Meta:
        model = Attachment
        # fields = '__all__'
        exclude = ('post', 'comment')
        read_only_fields = '__all__'
        depth = 1


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for facebook comment
    """
    id = serializers.ReadOnlyField()
    # comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comment-detail')
    user = FBUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = '__all__'
        # depth = 1


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialiser for facebook post
    """
    id = serializers.ReadOnlyField()
    # attachments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='attachment-detail')
    # comments = serializers.HyperlinkedIdentityField(many=True, read_only=True, view_name='comment-detail')
    # attachments = AttachmentSerializer(many=True, read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)
    user = FBUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = '__all__'
        # depth = 1


class BlacklistSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for blacklist
    """
    class Meta:
        model = Blacklist
        fields = '__all__'
        read_only_fields = '__all__'


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for report
    """
    id = serializers.ReadOnlyField()
    user = FBUserSerializer(read_only=True)
    group = GroupSerializer(required=True)
    post = PostSerializer(required=True)
    comment = CommentSerializer(required=True)
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = '__all__'
        # depth = 1


class BlacklistFBUserSerializer(FBUserSerializer):
    """
    Serializer for blacklist facebook user inherited Facebook User Serializer
    """
    blacklist = BlacklistSerializer(many=True, read_only=True)


class WardSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ward
    """
    id = serializers.ReadOnlyField()
    post = PostSerializer(required=True)
    comment = CommentSerializer(required=True)

    class Meta:
        model = Ward
        # fields = '__all__'
        read_only_fields = '__all__'
        exclude = ('user',)
        depth = 2


class UserActivitySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for user activity
    """
    user = FBUserSerializer(read_only=True)

    class Meta:
        model = UserActivity
        # fields = '__all__'
        read_only_fields = '__all__'
        exclude = ('group',)
        depth = 1
