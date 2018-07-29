from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Url(models.Model):
    actualUrl = models.URLField(max_length=1024)
    shortURL = models.URLField(max_length=1024)
