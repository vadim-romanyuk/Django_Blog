import datetime
import os.path

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from faker import Faker
from ckeditor.fields import RichTextField

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
    content = RichTextField()     #models.TextField()
    date = models.DateTimeField(auto_now_add=True)  #default=datetime.datetime.now   auto_now_add=True
    image = models.ImageField(upload_to= 'posta_img/%Y/%m/%d', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'posts'
        indexes = [
            models.Index(
                name='posts_date_time_idx',
                fields=['date']
            )
        ]
        ordering = ['-date']

    def __str__(self):
        return self.title
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            img = Post.objects.get(id=self.id).image
            if img and not self.image or img and self.image.path != img.path:
                print('удаляем старую картинку')
                if os.path.exists(img.path):
                    os.remove(img.path)
        except Post.DoesNotExist:
            pass
        return super(Post, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=500, null=True)
    hobby = models.CharField(max_length=300, null=True)


    class Meta:
        indexes = [
            models.Index(
                name='profile_idx',
                fields=['phone', 'address']
            )
        ]

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