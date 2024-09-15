from django.urls import path
from .views import *
from journalist.views import *
from editor.views import *
from head.views import *
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm

app_nane="users"

urlpatterns = [
    path('dashboard', ArticleListView.as_view(), name='dashboard'), 
    path('register/', register, name='register'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user_profile/', user_profile_view, name='user_profile'),
    path('journalist_dashboard/', journalist_dashboard, name='journalist_dashboard'),
    path('editor_dashboard/', editor_dashboard, name='editor_dashboard'),
    path('head_dashboard/', head_dashboard, name='head_dashboard'),
    path('review_article',review_article,name='review_article'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/<int:pk>/like/', like_article, name='like_article'),
    path('article/<int:pk>/comment/', add_comment, name='add_comment'),

    #PAssword
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
