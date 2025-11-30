from django.contrib import admin
from .models import Hotel, Comment


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'price_per_night', 'owner', 'created_at']
    list_filter = ['location', 'created_at', 'owner']
    search_fields = ['title', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'user', 'created_at', 'content_preview']
    list_filter = ['created_at', 'hotel']
    search_fields = ['content', 'user__username', 'hotel__title']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'