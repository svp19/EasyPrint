from django.db import models


# class RatePerPage(models.Model):
#
#     rate = models.SmallIntegerField(default=3)
#
#     def save(self, *args, **kwargs):
#         if RatePerPage.objects.count() > 1:
#             return
#
#         super(RatePerPage, self).save(*args, **kwargs)
