from django.db import models


class RatePerPage(models.Model):
    rppBW = models.FloatField(default=3)
    rppC = models.FloatField(default=5)
