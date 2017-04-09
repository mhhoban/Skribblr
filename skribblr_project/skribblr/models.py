from django.contrib.postgres.fields import JSONField
from django.db import models

class Author(models.Model):
    name = models.TextField(default='')

class Entry(models.Model):
    title = models.TextField(default='')
    author = models.ForeignKey(
        'Author',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(auto_now=False,auto_now_add=False)
    content = models.TextField(default='')
    tldr = models.TextField(default='')
