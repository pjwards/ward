from archive.models import FBUser, Group, Post, Comment, Media, Attachment, Blacklist, Report, Ward
from rest_framework import serializers

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"


# Serializers define the API representation.
class FBUserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comment-detail')
    posts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='post-detail')

    class Meta:
        model = FBUser
        fields = '__all__'
        read_only_fields = '__all__'


class ActivityFBUserSerializer(FBUserSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = FBUser
        exclude = ('posts', 'comments')
        read_only_fields = '__all__'


class ActivityForArchiveFBUserSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    picture = serializers.CharField()
    p_count = serializers.IntegerField()
    c_count = serializers.IntegerField()


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


class BlacklistSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Blacklist
        fields = '__all__'
        read_only_fields = '__all__'


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = '__all__'
        depth = 1


class BlacklistFBUserSerializer(FBUserSerializer):
    blacklist = BlacklistSerializer(many=True, read_only=True)


class WardSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Ward
        # fields = '__all__'
        read_only_fields = '__all__'
        exclude = ('user',)
        depth = 2
