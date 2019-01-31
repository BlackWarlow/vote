from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Poll(models.Model):
    date = models.DateField(default="2000-01-01")
    time = models.TimeField(default="00:00:00")
    name = models.CharField(max_length=100)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return 'poll <' + str(self.name) + '>'

class Poll_variant(models.Model):
    variant_name = models.CharField(max_length=100)
    votes = models.IntegerField()
    belongs_to = models.ForeignKey(
        to=Poll, default='none', on_delete=models.CASCADE)

class Author(models.Model):
    name = models.CharField(max_length=100)
    social = models.CharField(max_length=100)
    role = models.CharField(max_length=20, default='developer')

class Report_Model(models.Model):
    poll_id = models.ForeignKey(
        to=Poll, default='none', on_delete=models.CASCADE)
    type = models.CharField(max_length=200)
    text = models.TextField(max_length=5000)
    user = models.ForeignKey(to=User, default=1, on_delete=models.CASCADE)
