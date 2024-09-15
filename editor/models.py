from django.db import models
from users.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from journalist.models import Article


class Review(models.Model):
    article = models.ForeignKey('journalist.Article', on_delete=models.CASCADE)
    editor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)

        journalist_email = self.article.email
        subject = f"Article Review Status: {self.article.title}"
        
        if self.approved:
            message = f"Dear {self.article.author_name},\n\nYour article titled '{self.article.title}' has been approved by the editor."
        elif self.rejected:
            message = f"Dear {self.article.author_name},\n\nYour article titled '{self.article.title}' has been reviewed and unfortunately, it has been rejected by the editor."
        else:
            message = f"Dear {self.article.author_name},\n\nYour article titled '{self.article.title}' has been reviewed but is pending further action."

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [journalist_email],
            fail_silently=False,
        )
