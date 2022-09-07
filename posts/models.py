import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'posts'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    hobby = models.CharField(max_length=300, null=True)



class Log(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    obj = models.CharField('model', max_length=10)
    message = models.CharField(max_length=300)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('create_profile, sender:', sender)
    if created:
        Profile.objects.create(
            user=instance
        )
    print('create_profile, kwargs:', kwargs)


@receiver(post_save, sender=User)
def user_log(sender, instance, created, **kwargs):
    Log.objects.create(
        obj=sender.__class__.__name__,
        message=f'{instance.username} saved: {created}, with: {kwargs}'
    )