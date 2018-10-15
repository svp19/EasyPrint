from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


def get_sentinel_user():  # Sets a user to deleted when a task of a delete user is requested
    return get_user_model().objects.get_or_create(username='deleted')[0]


# sqlmigrate app 000x for SQL code of migrate
# for now, admin can control all tasks history
# need to add price to each thing
class PrintDocs(models.Model):
    ratePerPage = 3  # Rate per page in rupees, can add a model in AdminApp
    doc_name = models.CharField(max_length=500)
    pages = models.SmallIntegerField()
    copies = models.SmallIntegerField(default=1)
    completed = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    task_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))

    def __str__(self):
        return self.doc_name + ', ' + str(self.date_added)
