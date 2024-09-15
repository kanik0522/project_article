from django.urls import path
from . import views
from users.views import *

app_name = 'head'

urlpatterns = [
    # Dashboard
    path('head_dashboard/', views.head_dashboard, name='head_dashboard'),
    path('dashboard', ArticleListView.as_view(), name='dashboard'), 


    # Manage Users
    path('manage-users/', views.manage_users, name='manage_users'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('login/', login_view, name='custom_login'),
    path('article/<int:article_id>/', views.view_article, name='view_article'),
    path('logout/', logout_view, name='logout'),

    # Manage Articles
    path('manage-articles/', views.manage_articles, name='manage_articles'),
    path('edit-article/<int:pk>/', views.edit_article, name='edit_article'),
    path('delete-article/<int:pk>/', views.delete_article, name='delete_article'),
]
