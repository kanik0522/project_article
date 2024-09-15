from django.urls import path
from .views import *
from users.views import *
app_name = "editor"
urlpatterns = [
    path('login/', login_view, name='login_view'),
    path('dashboard', ArticleListView.as_view(), name='dashboard'), 

    path('editor_dashboard/', editor_dashboard, name='editor_dashboard'),
    path('review/<int:article_id>/', review_article, name='review_article'),
    path('article/<int:article_id>/', show_article, name='show_article'),

]
