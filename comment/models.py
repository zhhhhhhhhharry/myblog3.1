# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from article.models import ArticleInf

# 博文的评论
class Comment(models.Model):
    article = models.ForeignKey(ArticleInf, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body[:20]