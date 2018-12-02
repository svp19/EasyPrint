import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


def get_sentinel_user():  # Sets a user to deleted when a task of a delete user is requested
    return get_user_model().objects.get_or_create(username='deleted')[0]


# sqlmigrate app 000x for SQL code of migrate

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount_due = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    hash_url = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class PrintDocs(models.Model):
    description = models.CharField(max_length=255, default='')
    document = models.FileField(upload_to=settings.EASY_PRINT_MEDIA_DIR)
    file_name = models.CharField(max_length=500, default='no_name_given')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    colour = models.BooleanField(default=False)  # 0 for black
    copies = models.SmallIntegerField(default=1)
    task_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    num_pages = models.SmallIntegerField(default=1)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    completed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    collected = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    order_id = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.document.name

    class Meta:
        verbose_name = 'Document'  # Name of registered model in Admin panel
