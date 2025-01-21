from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.shortcuts import render,redirect
from comment.models import Comment
from . import models
from .models import ArticleInf
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q

def article_all(request):
    search_query = request.GET.get('search', '')  # 获取搜索关键词
    if search_query:
        article_list = ArticleInf.objects.filter(Q(title__icontains=search_query)|Q(body__icontains=search_query)|Q(total_views__icontains=search_query))
    else:
        article_list = ArticleInf.objects.all()

    # 分页
    paginator = Paginator(article_list, 6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {
        'articles': articles,
        'order': 'normal',
        'search_query': search_query,
    }
    return render(request, 'article_list.html', context)

@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == 'POST':
        new_article_title = request.POST.get('title')
        new_article_body = request.POST.get('body')
        new_article_author = request.user

        if not new_article_title or not new_article_body:
            messages.error(request, '标题和内容不能为空！')
            return render(request, 'article_create.html')

        models.ArticleInf.objects.create(
            title=new_article_title,
            body=new_article_body,
            author=new_article_author
        )

        messages.success(request, '文章创建成功！')
        return redirect("article:article_all")

    return render(request, 'article_create.html')



def article_detail(request, id):
    article = ArticleInf.objects.get(id=id)
    article.total_views += 1
    article.save(update_fields=['total_views'])
    comments = Comment.objects.filter(article=id)
    context = { 'article': article, 'comments': comments }
    return render(request, 'article_detail.html', context)

@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    article = ArticleInf.objects.get(id=id)
    if request.user != article.author:
        messages.error(request, "你无权删除这篇文章。")
        return redirect("article:article_detail")
    else:
        article.delete()
        return redirect("article:article_all")

@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = ArticleInf.objects.get(id=id)
    if request.user != article.author:
        messages.error(request,"抱歉，你无权修改这篇文章。")
        return redirect("article:article_detail",id=id)

    if request.method == "POST":
        new_article_title = request.POST.get('title')
        new_article_body = request.POST.get('body')
        article.title = new_article_title
        article.body = new_article_body
        article.save()
        messages.success(request,"文章修改成功")
        return redirect("article:article_detail", id=id)
    else:
        context = {'article': article}
        return render(request, 'article_update.html', context)