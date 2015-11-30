from django.contrib import admin

from .models import User, Group, Post, Comment, Media, Attachment, Blacklist, DeletedPost, DeletedComment, Report, Ward


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
    search_fields = ['user']


class WardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'group', 'post', 'comment', 'created_time', 'updated_time')


admin.site.register(User, UserAdmin)
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
