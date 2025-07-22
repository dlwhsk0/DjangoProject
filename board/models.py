from django.db import models

class Board(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 최초 저장 시에만 현재 날짜
    updated_at = models.DateTimeField(auto_now=True) # 수정이 될 때마다 현재 날짜
    deleted_at = models.DateTimeField(default=None, null=True)

class Comment(models.Model):
    board = models.ForeignKey('Board', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}: {self.content[:20]}"