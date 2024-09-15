from django.urls import path
from .views import *
from users.views import *

app_name = 'journalist'

urlpatterns = [
    path('journalist_dashboard/', journalist_dashboard, name='journalist_dashboard'),
    path('journalist_dashboard_step1/', journalist_dashboard_step1, name='journalist_dashboard_step1'),
    path('journalist_dashboard_step2/', journalist_dashboard_step2, name='journalist_dashboard_step2'),
    path('login/', login_view, name='login_view'),
    path('dashboard', ArticleListView.as_view(), name='dashboard'), 
    path('logout/', j_logout, name='logout'),
    path('user_profile/', user_profile_view, name='user_profile'),

    path('edit/<int:article_id>/', edit_article, name='edit_article'),
    path('delete/<int:article_id>/', delete_article, name='delete_article'),
    
]
