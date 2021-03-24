from django.contrib import admin
from posts.models import Post, PostImage, Likes

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1   

class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]
    readonly_fields = ('date', )

admin.site.register(Post, PostAdmin)
admin.site.register(Likes)
