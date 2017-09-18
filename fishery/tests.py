from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    cases = ['successful', 'out_of_fish']

    def play_round(self):
        yield (views.Introduction)

        if self.case == 'successful':

        else:


        yield (views.Results)
