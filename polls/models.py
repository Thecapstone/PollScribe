import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    path_count = models.IntegerField(default = 0)
    branches = models.IntegerField(default = 0)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now 
    
    class Meta:
        ordering = ['pub_date']


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
class FollowUpQuestion(models.Model):
    parent_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="new_branch", null=True, blank=True)
    parent_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="extra_questions", null=True, blank=True)
    # a self-reference object allowing for responses to other responses (similar to comments) 
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    path_count = models.IntegerField(default = 0)
    content = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ['pub_date']
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
class FollowUpChoices(models.Model):
    related_question = models.ForeignKey(FollowUpQuestion, on_delete=models.CASCADE, related_name='choices', null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    

    def __str__(self):
        return self.content