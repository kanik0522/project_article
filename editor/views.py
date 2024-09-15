from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review
from journalist.models import Article
from users.decorators import role_required
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.conf import settings



@role_required('editor')
def editor_dashboard(request):
    submitted_articles = Article.objects.filter(status='submitted')
    reviewed_articles = Article.objects.exclude(status='submitted')
    return render(request, 'editor_dashboard.html', {
       
   
        'submitted_articles': submitted_articles,
        'reviewed_articles': reviewed_articles,
       })

def logout_view(request):
    auth_logout(request)
    request.session.flush()

    return redirect('login_view')

@role_required('editor')
def review_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    journalist_email = article.email  # Use the email provided by the journalist

    if request.method == 'POST':
        action = request.POST.get('action')
        subject = f"Article Review Status: {article.title}"

        if action == 'accept':
            article.status = 'accepted'
            article.save()

            # Send approval email
            message = f"Dear {article.author_name},\n\nYour article titled '{article.title}' has been approved by the editor."
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [journalist_email],
                fail_silently=False,
            )
            return redirect('editor:editor_dashboard')

        elif action == 'reject':
            article.status = 'rejected'
            article.save()

            # Send rejection email
            message = f"Dear {article.author_name},\n\nYour article titled '{article.title}' has been rejected by the editor."
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [journalist_email],
                fail_silently=False,
            )
            return redirect('editor:editor_dashboard')

    return render(request, 'review_article.html', {'article': article})



@role_required('editor')
def show_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'show_article.html', {'article': article})


@login_required
def article_review_list(request):
    articles = Article.objects.filter(is_published=False)
    return render(request, 'article_review_list.html', {'articles': articles})

