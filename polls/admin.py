from django.contrib import admin

from .models import Question, FollowUpQuestion, Choice, FollowUpChoices

admin.site.register(Question)
admin.site.register(FollowUpQuestion)
admin.site.register(Choice)     
admin.site.register(FollowUpChoices)

# Register your models here.
