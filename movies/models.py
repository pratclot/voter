# from django.db import models
#
# # Create your models here.
from django.db import models
from social_django.models import USER_MODEL
from pprint import pprint


class Answer(models.Model):
    answer_text = models.CharField(max_length=200)

    def __str__(self):              
        return self.answer_text


class Poll(models.Model):
    poll_question = models.CharField(max_length=200)
    poll_date = models.DateTimeField('poll date')
    answers = models.ManyToManyField(Answer, through='PollVotes')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # first, save normally, so the object exists
        super(Poll, self).save(force_insert=force_insert,
                               force_update=force_update, using=using,
                               update_fields=update_fields)

        # then add some conversationalists
        if self.answers.count() < 1:
            new_answers = Answer.objects.order_by('?')[:5].filter()
            [PollVotes.objects.create(poll=self,
                                      answer=x) for x in new_answers]
            # self.answers.add(new_answer)

    def __str__(self):              
        return self.poll_question


class PollVotes(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)


class PollVoters(models.Model):
    username = models.ForeignKey(USER_MODEL,
                                 on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
