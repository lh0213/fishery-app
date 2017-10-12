from otree.api import Currency as c, currency_range, SubmissionMustFail, Submission

import result
from . import views
from ._builtin import Bot
from random import randint
from .models import Constants


class PlayerBot(Bot):
    cases = ['greedy', 'lazy', 'normal']

    def play_round(self):

        # do not submit anything, send error
        # yield SubmissionMustFail(views.StudentCatch)

        fish = {
            'greedy': 2,
            'lazy': 0,
            'normal': randint(0, 2),
        }[self.case]

        # timeout happened?
        # yield (views.StudentCatch, {'num_fish_caught_this_year': fish}, timeout_happened)

        yield (views.StudentCatch, {'num_fish_caught_this_year': fish})

        if self.subsession.num_fish_at_start_of_year > 0:
            yield (views.StudentFinalResult)
        else:
            yield Submission(result.views.Result, {}, check_html=False)
