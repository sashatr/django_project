from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()

    last_updated = models.DateTimeField(default=timezone.now)         #auto_now=False
    published_date = models.DateTimeField(blank=True, null=True)

    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title + ' -> ' + str(self.author)
