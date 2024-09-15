from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from journalist.models import Article
from editor.models import Review  # Assuming there's a Review model in the editor app
from head.forms import UserProfileForm, CustomUserForm
from users.decorators import role_required
from django.contrib.auth import logout as auth_logout


# Admin Dashboard
@role_required('head')
def head_dashboard(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'head_dashboard.html', context)

def logout_view(request):
    auth_logout(request)
    request.session.flush()

    return redirect('login')


@role_required('head')
def view_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'view_article.html', {'article': article})



User = get_user_model()

@role_required('head')

def manage_users(request):
    if not request.user.is_authenticated or not (request.user.is_head or request.user.is_superuser):
        return redirect('login')
    
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'manage_users.html', context)

@role_required('head')

def user_detail(request, user_id):
    if not request.user.is_authenticated or not (request.user.is_head or request.user.is_superuser):
        return redirect('login')
    
    user = get_object_or_404(User, id=user_id)
    return render(request, 'head/user_detail.html', {'user': user})

@role_required('head')

def edit_user(request, user_id):
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('head:manage_users')
    else:
        form = CustomUserForm(instance=user)
    
    return render(request, 'edit_user.html', {'form': form})

@role_required('head')

def delete_user(request, user_id):
    if not request.user.is_authenticated or not (request.user.is_head or request.user.is_superuser):
        return redirect('login')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.delete()
        return redirect('head:manage_users')
    
    return render(request, 'head/delete_user.html', {'user': user})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from journalist.models import Article
from head.forms import ArticleForm

@role_required('head')

def manage_articles(request):
    if not request.user.is_authenticated or not (request.user.is_head or request.user.is_superuser):
        return redirect('login')
    
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'manage_articles.html', context)



@role_required('head')
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('manage_articles')  # Ensure this URL exists and is correct
        else:
            # Show form errors if validation fails
            print(form.errors)  # Debugging step to see errors in the console
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'head/edit_article.html', {'form': form, 'article': article})

@role_required('head')
def delete_article(request, article_id):
    if not request.user.is_authenticated or not (request.user.is_head or request.user.is_superuser):
        return redirect('login')
    
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        article.delete()
        return redirect('manage_articles')
    
    return render(request, 'head/delete_article.html', {'article': article})
