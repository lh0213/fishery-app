from otree.api import Currency as c, currency_range, SubmissionMustFail
from otree.constants_internal import timeout_happened

from . import views
from ._builtin import Bot
from .models import Constants
from random import randint



class PlayerBot(Bot):
    cases = ['greedy', 'lazy', 'normal']

    @property
    def play_round(self):

        # do not submit anything, send error
        yield SubmissionMustFail(views.StudentCatch)

        fish = {
            'greedy': 2,
            'lazy': 0,
            'normal': randint(0, 2),
        }[self.case]

        # timeout happened?
        # yield (views.StudentCatch, {'num_fish_caught_this_year': fish}, timeout_happened)

        yield (views.StudentCatch, {'num_fish_caught_this_year': fish})
        yield (views.OutOfFishResult)
        yield (views.StudentFinalResult)

