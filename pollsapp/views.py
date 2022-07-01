from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponseRedirect

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from django.urls import reverse
from django.views import generic

from django.utils import timezone

from .models import Question

from django.http import Http404


class IndexView(generic.ListView):
    template_name = 'pollsapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
# Leave the rest of the views (detail, results, vote) unchanged
class DetailView(generic.DetailView):
    model = Question
    template_name = 'pollsapp/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'pollsapp/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'pollsapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('pollsapp:results', args=(question.id,)))