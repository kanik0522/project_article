from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Article(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('published', 'Published'),
    ]

    CATEGORY_CHOICES = [
        ('news', 'News'),
        ('opinion', 'Opinion'),
        ('trends', 'Trends'),
    ]

    TAG_CHOICES = [
        ('politics', 'Politics'),
        ('tech', 'Tech'),
        ('sports', 'Sports'),
        ('fun', 'Fun'),
    ]

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    content = models.TextField()
    author_name = models.CharField(max_length=100, default='Unknown Author')  # Make sure this matches
    email = models.EmailField(null=True)  # Ensure this field is correctly populated
    image = models.ImageField(upload_to='articles/images/', blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_date = models.DateField()
    agree_terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    article = models.ForeignKey(Article, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('article', 'user')

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"
