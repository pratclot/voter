from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from pprint import pprint
import logging

from .models import Poll, PollVoters, PollVotes, Answer
from django.contrib.auth.models import User

logger = logging.getLogger('django')


class AuthListView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


class AuthDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


class PollsView(LoginRequiredMixin, generic.ListView, ):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'movies/polls.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Poll.objects.order_by('-poll_date')[:5]


class PollDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Poll
    template_name = 'movies/poll_detail.html'
    context_object_name = 'question'


class PollResultsView(AuthDetailView):
    model = Poll
    template_name = 'movies/poll_results.html'
    context_object_name = 'poll'

    def get_context_data(self, **kwargs):
        ctx = super(PollResultsView, self).get_context_data(**kwargs)
        ctx['poll_votes'] = {x: Answer.objects.get(pk=x.answer_id) for x in
                             PollVotes.objects.filter(
                                 poll_id=ctx[
                                     self.context_object_name]).only(
                                 'id',
                                 'answer_id')
                             }
        ctx['answers'] = [x.answer_text for x in ctx['poll_votes'].values()]
        #        logger.debug(ctx['answers'])
        #        [logger.debug(x) for x in ctx['answers']]
        ctx['votes'] = [x.votes for x in ctx['poll_votes'].keys()]
        ctx['chart_data'] = [{'name': y.answer_text, 'value': x.votes}
                             for x, y in ctx['poll_votes'].items()]
        ctx['chart_selected'] = {y.answer_text: x.votes
                                 for x, y in ctx['poll_votes'].items()}
        username_ids = PollVoters.objects.filter(
            poll_id=ctx[
                self.context_object_name
            ]
        ).only('username_id')
        pprint(username_ids)
        pprint(User.objects.all().only('id', 'username'))
        ctx['voters'] = {x.username: 1 if y.username_id == x.id else 0
                         for x in User.objects.all().only('id', 'username')
                         for y in username_ids}
        pprint(ctx['voters'])
        return ctx

    # @login_required
    def home(request):
        return render(request, 'home.html')

    # def login(request):
    # 	return render(request, 'registration/login.html')
    #
    # def logout(request):
    # 	return render(request, 'registration/logout.html')


def vote2(request, poll_id):
    question = get_object_or_404(Poll, pk=poll_id)
    try:
        selected = request.POST.getlist('choice')
    except Exception as e:
        print(e)
    selected_choice = [
        question.answers.get(pk=x) for x in selected
    ]
    if len(selected_choice) == 0:
        return render(request, 'movies/poll_detail.html', {
            'question': question,
            'error_message': "You did not choose anything, dummy.",
        })
    else:
        try:
            voters = PollVoters.objects.filter(poll_id=poll_id,
                                               username_id=request.user.id)
            if not voters:
                PollVoters.objects.create(poll_id=poll_id,
                                          username_id=request.user.id)
                for x in selected_choice:
                    current_vote = PollVotes.objects.get(answer_id=x.id,
                                                         poll_id=poll_id)
                    current_vote.votes += 1
                    current_vote.save()
            else:
                return render(request, 'movies/cheater.html')
        except Exception as e:
            pprint(e)
            raise

    return HttpResponseRedirect(
        reverse('movies:poll_results', args=(question.id,)))
