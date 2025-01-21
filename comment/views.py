
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from article.models import ArticleInf
from . import models
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from .models import  Comment

@login_required(login_url='/users_profile_app/login/')
def post_comment(request, article_id):
    article = get_object_or_404(ArticleInf, id=article_id)
    if request.method == 'POST':
        new_comment_body = request.POST.get('body')
        if not new_comment_body:
            messages.error(request, "评论内容不能为空！")
            return redirect(article)

        new_article_user = request.user
        Comment.objects.create(article=article, body=new_comment_body, user=new_article_user)

        article.comment_count +=1
        article.save()

        messages.success(request, "评论发表成功！")  # 添加成功消息
        return redirect(article)

