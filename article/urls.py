from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'article'

urlpatterns = [
    path('', views.article_all, name='article_all'),
    path('article-all/', views.article_all, name='article_all'),
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    path('article-create/', views.article_create, name='article_create'),
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'),
    path('article-update/<int:id>/', views.article_update, name='article_update'),

]