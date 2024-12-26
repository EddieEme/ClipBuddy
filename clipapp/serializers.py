from rest_framework import serializers
from .models import Snippet

class SnippetSerializer(serializers.ModelSerializer):
    def validate_tags(self, value):
        if isinstance(value, str):
            # Split string into list if comma-separated string is received
            value = [tag.strip() for tag in value.split(',') if tag.strip()]
        if not isinstance(value, (list, set)):
            raise serializers.ValidationError("Tags must be a list or comma-separated string.")
        return list(value)

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'description', 'content', 'tags', 'favorite', 'created_at', 'updated_at', 'user']
        read_only_fields = ['created_at', 'updated_at', 'user']
