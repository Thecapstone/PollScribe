from django.db.models import F
from django.http import HttpResponseRedirect, Http404 
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

# rest imports
from rest_framework import permissions, status
from rest_framework. permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

# polls imports
from .serializers import QuestionSerializer, CreateQuestionSerializer, CreateFollowUpQuestionSerializer, CreateChoiceSerializer
from .permissions import IsAuthorOrReadOnly
from .models import Choice, Question, FollowUpQuestion



class PollList(APIView):
    """
    Returns a templated HTML response for all available polls.
    """
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]
    template_name='polls/index.html'

    def get(self, request, *args, **kwargs):
        queryset = Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:10]
        return Response({'latest_question_list':queryset})

class NewPoll(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'polls/create_poll.html'

    def post(self, request):
        serializer = CreateQuestionSerializer(data=request.data)

        if serializer.is_valid():
            question = serializer.save(
                author = request.user,
                pub_date = timezone.now()
            )

            choices = request.data.getlist("choices")
            for text in choices:
                Choice.objects.create(
                    question = question,
                    choice_text = text
                )
            return Response({"question": question}, status = 201)
        return render(
            "polls/index.html",
            {"errors": serializer.errors},
            status = 400
        )




class PollDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'polls/detail.html'

    def get_object(self, pk):
        return get_object_or_404(Question, pk=pk)

    def get(self, request, pk):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response({'serializer': serializer, 'question': question})
    
    def post(self, request, pk):
        question = self.get_object(pk)
        serializer = CreateQuestionSerializer(question)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'question': question})
        serializer.save()
        return redirect('polls/index')


    def put(self, request, data, pk):
        question = self.get_object(pk)
        self.check_object_permissions(request, question)

        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_404_BAD_REQUEST)
        
    def delete(self, request, pk):
        question = self.get_object(pk)
        self.check_object_permissions(request, question)

        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
class Branch(APIView):
    """
    Defines an alternative question path to the original question; 
     Allows the writer to create a new branch of thought following the same topic
    """
    def get_object(self, pk):
        return get_object_or_404(Question, pk=pk)

    #create followup question to the original question and increment path count
    def post(self, request, pk):
        question = self.get_object(pk)
        serializer = CreateFollowUpQuestionSerializer(
            data=request.data, 
            context={"request": request, "parent_question": question})

        if serializer.is_valid():
            serializer.save(author=request.user, parent_question=question)
            Question.objects.filter(pk=pk).update(branches = F("branches") + 1)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Path(APIView):
    """
    Defines a new question as an extension to a choice defined by the original author; 
     Allows the writer to expand on the thought process in a selected choice.
    """
    def get_object(self, pk):
        return get_object_or_404(Choice, pk=pk)
    
    def post(self, request, pk):
        choice = self.get_object(pk)
        serializer = CreateFollowUpQuestionSerializer(
            data=request.data,
            context={"request": request, "parent_choice": choice}
        )
        if serializer.is_valid():
            serializer.save(author=request.user, parent_choice= choice)
            Question.objects.filter(pk=pk).update(path_count = F("path_count") + 1)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

   


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # If the question has any follow-up questions, redirect to the
        # followup's own ID; otherwise go to the results page.
        followups = question.extra_questions.all()
        if followups.exists():
            followup = followups.first()
            return HttpResponseRedirect(reverse("polls:followup", args=(followup.id,)))

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def followupquestionDisplay(request, pk):
    followup = get_object_or_404(FollowUpQuestion, id=pk)
    return render(request, "polls/followupdetail.html", {"followup": followup})