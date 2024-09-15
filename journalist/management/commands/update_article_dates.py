# your_app/management/commands/update_article_dates.py
from django.core.management.base import BaseCommand
from journalist.models import Article
from django.utils import timezone

class Command(BaseCommand):
    help = 'Update created_at field for existing articles'

    def handle(self, *args, **kwargs):
        default_date = timezone.now()
        Article.objects.filter(created_at__isnull=True).update(created_at=default_date)
        self.stdout.write(self.style.SUCCESS('Successfully updated created_at for existing articles.'))
