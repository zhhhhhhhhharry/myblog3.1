from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField


# 博客文章数据模型
class ArticleInf(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = HTMLField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    comment_count=models.PositiveIntegerField(default=0)
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title

        # 获取文章地址
    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])