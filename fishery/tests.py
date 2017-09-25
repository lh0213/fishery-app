from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import views
from ._builtin import Bot
from .models import Constants
from random import randint



class PlayerBot(Bot):

    @property
    def play_round(self):

        # do not submit anything, send error
        yield SubmissionMustFail(views.StudentCatch)

        yield (views.StudentCatch, {'num_fish_caught_this_year': randint(0, 2)})
        yield (views.OutOfFishResult)
        yield (views.StudentFinalResult)

