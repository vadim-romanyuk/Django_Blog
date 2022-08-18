import datetime

from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length= 100)
    content = models.TextField()
    date = models.DateTimeField(default= datetime.datetime.now)
