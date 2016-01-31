# The MIT License (MIT)
#
# Copyright (c) 2015 pjwards.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==================================================================================
""" Sets an admin site """

from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'picture')
    list_filter = ['name']
    search_fields = ['name']


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'updated_time', 'privacy', 'is_stored')
    list_filter = ['updated_time']
    search_fields = ['name']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'message', 'picture']}),
        ('Date information', {'fields': ['created_time', 'updated_time'], 'classes': ['collapse']}),
    ]
    inlines = [CommentInline]
    list_display = (
    'id', 'user', 'created_time', 'updated_time', 'message', 'comment_count', 'like_count', 'is_show')
    list_filter = ['created_time', 'updated_time']
    search_fields = ['message']


class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'message']}),
        ('Date information', {'fields': ['created_time'], 'classes': ['collapse']}),
    ]
    inlines = [CommentInline]
    list_display = ('id', 'user', 'created_time', 'message', 'comment_count', 'like_count', 'is_show')
    list_filter = ['created_time']
    search_fields = ['message']


class MediaAdmin(admin.ModelAdmin):
    list_display = ('src', 'height', 'width')


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'type', 'url')


class BlacklistAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_group', 'count', 'updated_time')
    list_filter = ['updated_time']
    search_fields = ['user__name']

    def get_user(self, obj):
        return obj.user.name
    get_user.short_description = 'User'
    get_user.admin_order_field = 'user__name'

    def get_group(self, obj):
        return obj.group.name
    get_group.short_description = 'Group'
    get_group.admin_order_field = 'group__name'


class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'post', 'comment', 'updated_time', 'status')


class DeletedPostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'message', 'picture']}),
        ('Date information', {'fields': ['created_time', 'updated_time'], 'classes': ['collapse']}),
    ]
    list_display = (
    'id', 'user', 'created_time', 'updated_time', 'message', 'comment_count', 'like_count', 'share_count')
    list_filter = ['created_time', 'updated_time']
    search_fields = ['message']


class DeletedCommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'message']}),
        ('Date information', {'fields': ['created_time'], 'classes': ['collapse']}),
    ]
    list_display = ('id', 'user', 'created_time', 'message', 'comment_count', 'like_count')
    list_filter = ['created_time']
    search_fields = ['user__id']


class WardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'post', 'comment', 'created_time', 'updated_time')


class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'post_count', 'comment_count')
    search_fields = ['user__id', 'group__id']


class GroupStoreListAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'start_time', 'end_time', 'query', 'status')


class InterestGroupListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group')


admin.site.register(FBUser, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Blacklist, BlacklistAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(DeletedPost, DeletedPostAdmin)
admin.site.register(DeletedComment, DeletedCommentAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(UserActivity, UserActivityAdmin)
admin.site.register(GroupStoreList, GroupStoreListAdmin)
admin.site.register(InterestGroupList, InterestGroupListAdmin)
