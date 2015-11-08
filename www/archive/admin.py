from django.contrib import admin

from .models import User, Group, Post, Comment, Media, Attachment


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
    'id', 'user', 'created_time', 'updated_time', 'message', 'comment_count', 'like_count', 'share_count')
    list_filter = ['created_time', 'updated_time']
    search_fields = ['user']


class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'message']}),
        ('Date information', {'fields': ['created_time'], 'classes': ['collapse']}),
    ]
    inlines = [CommentInline]
    list_display = ('id', 'user', 'created_time', 'message', 'comment_count', 'like_count')
    list_filter = ['created_time']
    search_fields = ['user']


class MediaAdmin(admin.ModelAdmin):
    list_display = ('src', 'height', 'width')


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'type', 'url')


admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Attachment, AttachmentAdmin)
