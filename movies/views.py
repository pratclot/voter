from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from pprint import pprint

from .models import Choice, Question, Voters


class AuthListView(LoginRequiredMixin, generic.ListView):
    pass


class AuthDetailView(LoginRequiredMixin, generic.DetailView):
    pass


class IndexView(AuthListView):
    template_name = 'movies/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(AuthDetailView):
    model = Question
    template_name = 'movies/detail.html'


class ResultsView(AuthDetailView):
    model = Question
    template_name = 'movies/results.html'


def vote(request, question_id):
    ...  # same as above, no changes needed.
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected = request.POST.getlist('choice')
    except Exception as e:
        print(e)
    try:
        selected_choice = [
            question.choice_set.get(pk=x) for x in selected
        ]
        if len(selected_choice) == 0:
            return render(request, 'movies/detail.html', {
                'question': question,
                'error_message': "You did not choose anything.",
            })
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'movies/detail.html', {
            'question': question,
            'error_message': "You did not choose anything.",
        })
    else:
        try:
            voters = Voters.objects.filter(question_id=question_id,
                                           username_id=request.user.id)
            pprint(voters)
            if not voters:
                Voters.objects.create(question_id=question_id,
                                      username_id=request.user.id)
                for x in selected_choice:
                    x.votes += 1
                    x.save()
            else:
                return render(request, 'movies/cheater.html')
        except Exception as e:
            pprint(e)
            raise

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('movies:results', args=(question.id,)))


# @login_required
def home(request):
    return render(request, 'home.html')

# def login(request):
# 	return render(request, 'registration/login.html')
#
# def logout(request):
# 	return render(request, 'registration/logout.html')
