from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Poll(models.Model):
    hash_id = models.CharField(max_length=20)
    date = models.DateField(default="2000-01-01")
    open_date = models.DateField(default="2001-01-01")
    time = models.TimeField(default="00:00:00")
    name = models.CharField(max_length=100)
    one_answer = models.BooleanField(default=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return 'poll <' + str(self.name) + '>'

class Poll_variant(models.Model):
    variant_name = models.CharField(max_length=100)
    belongs_to = models.ForeignKey(
        to=Poll, default='none', on_delete=models.CASCADE)

class Vote(models.Model):
    belongs_to = models.ForeignKey(
        to=Poll_variant, default='none', on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

class Author(models.Model):
    name = models.CharField(max_length=100)
    social = models.CharField(max_length=100)
    role = models.CharField(max_length=20, default='developer')

class Report_Model(models.Model):
    poll = models.ForeignKey(
        to=Poll, default='none', on_delete=models.CASCADE)
    theme = models.CharField(max_length=200)
    text = models.TextField(max_length=5000)
    user = models.ForeignKey(to=User, default=1, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)

class Blog_Model(models.Model):
    theme = models.CharField(default='theme', max_length=30)
    author = models.ForeignKey(to=User, default=1, on_delete=models.CASCADE)
    date = models.DateField(default='2000-01-01')
    content = models.CharField(default='<p>text</p>', max_length=1500)