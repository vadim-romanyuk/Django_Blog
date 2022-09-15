import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from faker import Faker

# Create your models here.


# class Base(models.Model):
#     title = models.CharField(max_length=100)
#     text = models.TextField()
#
#     class Meta:
#         abstract = True
#
#
# class Comments(Base):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     title = None
#
#     class Meta(Base.Meta):
#         abstract = True


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
    address = models.CharField(max_length=500, null=True)
    hobby = models.CharField(max_length=300, null=True)


# class Log(models.Model):
#     datetime = models.DateTimeField(auto_now_add=True)
#     obj = models.CharField('model', max_length=1000)
#     message = models.CharField('model', max_length=1000)



class Log(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    obj = models.CharField('model', max_length=10)
    message = models.CharField(max_length=300)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # print('create_profile, sender:', sender)
    if created:
        print('created', instance)
        f = Faker('ru_RU')
        Profile.objects.create(
            user=instance,
            phone=f.phone_number(),
            address=str(f.address())
        )
    # print('create_profile, kwargs:', kwargs)


@receiver(post_save, sender=User)
def user_log(sender, instance, created, **kwargs):
    Log.objects.create(
        obj=sender.__class__.__name__,
        message=f'{instance.username} saved: {created}, with: {kwargs}'
    )


@receiver(post_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    Log.objects.create(
        obj=str(type(sender))[:10],
        message=f'{instance.username} has been deleted | {kwargs}'
    )