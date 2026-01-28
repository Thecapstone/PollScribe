from rest_framework import serializers
from .models import Question, FollowUpQuestion, Choice, FollowUpChoices

class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["question_text", "choices"]

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text", "author", "pub_date", "path_count"]

class QuestionSerializer(serializers.ModelSerializer):
    #new_branch and extra_questions are not direct fields of the Questions model but are foreign key relationships from the FollowUpQuestions model.
    class Meta:
        model = Question
        fields = ["question_text", "author", "pub_date","choices","branches", "path_count"]

class CreateChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['choices', "choice_text"]

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "choice_text", "votes"]

class CreateFollowUpQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUpQuestion
        fields = ["id", "content", "author", "pub_date"]

class FollowUpQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUpQuestion
        fields = ["id", "content", "author", "pub_date", "choices", "path_count"]

class FollowUpChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUpChoices
        fields = ["id", "content"]