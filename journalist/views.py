from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleStep1Form, ArticleStep2Form
from head.forms import ArticleForm
from users.decorators import role_required
from django.apps import apps
from django.contrib.auth import logout as auth_logout

@role_required('journalist')
def journalist_dashboard(request):
    user = request.user
    articles = Article.objects.filter(email=user.email).order_by('-created_at')
    full_name = f"{user.first_name} {user.last_name}"
    return render(request, 'journalist_dashboard.html', {
        'user': user,
        'articles': articles,
    })

def j_logout(request):
    auth_logout(request)
    request.session.flush()

    return redirect('journalist:login_view')

@role_required('journalist')
def journalist_dashboard_step1(request):
    if request.method == 'POST':
        form = ArticleStep1Form(request.POST, user_email=request.user.email)  # Pass the email for POST request
        if form.is_valid():
            request.session['article_data'] = form.cleaned_data
            return redirect('journalist:journalist_dashboard_step2')
    else:
        form = ArticleStep1Form(user_email=request.user.email)  # Pass the email for GET request
    return render(request, 'journalist_dashboard_step1.html', {'form': form})

@role_required('journalist')
def journalist_dashboard_step2(request):
    if request.method == 'POST':
        form = ArticleStep2Form(request.POST, request.FILES)
        if form.is_valid():
            article_data = request.session.get('article_data', {})
            if not isinstance(article_data, dict):
                article_data = {}
            article_data.update(form.cleaned_data)

            tags = article_data.pop('tags', None)
            category_name = article_data.pop('category', None)
            if category_name:
                Category = apps.get_model('journalist', 'Category')
                category, created = Category.objects.get_or_create(name=category_name)
                article_data['category'] = category

            article = Article.objects.create(**article_data)
            if tags is not None:
                article.tags.set(tags)

            del request.session['article_data']
            return redirect('journalist:journalist_dashboard')
    else:
        form = ArticleStep2Form()
    article_data = request.session.get('article_data', {})
    for field in form.fields:
        form.fields[field].initial = article_data.get(field, None)
    return render(request, 'journalist_dashboard_step2.html', {'form': form})



@role_required('journalist')
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('journalist:journalist_dashboard')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit_article.html', {'form': form, 'article': article})


@role_required('journalist')
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect('journalist_dashboard')
    return render(request, 'delete_article.html', {'article': article})

