from django.contrib import admin
from . models import *

@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'favorite', 'created_at', 'updated_at')
    list_filter = ('favorite', 'tags', 'created_at')
    search_fields = ('title', 'description', 'tags')

@admin.register(UserTestimonial)
class  UserTestimonialAdmin(admin.ModelAdmin):
    list_display = ('text',)