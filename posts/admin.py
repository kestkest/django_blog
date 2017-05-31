from django.contrib import admin
from .models import Post, Tag, PostComment


class PostCommentInline(admin.TabularInline):
    model = PostComment
    fields = ('author', 'post', 'content')
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = [PostCommentInline, ]
    list_display = ('title', 'author', 'created',)
    list_filter = ('created', 'author')
    fieldsets = (
        (None, {'fields': ('title', 'body', 'author')}),
    )
    search_fields = ('author__username', 'title', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_filter = ('name',)
    fieldsets = (
        ('Tag fields', {'fields': ('name', 'post')}),
    )


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    fields = ('author', 'content')
    list_filter = ('author', 'post', )
    list_display = ('author', 'created', )
    search_fields = ('author__username',)
