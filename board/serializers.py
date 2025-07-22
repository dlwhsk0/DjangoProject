from rest_framework import serializers
from .models import Board
from .models import Comment

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'deleted_at']

class BoardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['title', 'content']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'board', 'author', 'content', 'created_at', 'updated_at']