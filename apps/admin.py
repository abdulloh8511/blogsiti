from django.contrib import admin
from .models import User, Category, Blog, Comment, Profile, Tag, BlogLike

admin.site.site_header = "BlogSite Admin"
admin.site.site_title = "BlogSite Admin"
admin.site.index_title = "BlogSite boshqaruvi"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active']
    search_fields = ['username', 'email']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    filter_horizontal = ['tags']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'blog', 'created_at']
    search_fields = ['content', 'author__username', 'blog__title']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'views']
    search_fields = ['user__username']


@admin.register(BlogLike)
class BlogLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'created_at']
    search_fields = ['user__username', 'blog__title']
