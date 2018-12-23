# from django.db import models
#
# # Create your models here.
from django.db import models
from social_django.models import USER_MODEL


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class Voters(models.Model):

    username = models.ForeignKey(USER_MODEL,
                                 on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
