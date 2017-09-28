from otree.api import Currency as c, currency_range, Submission

import fishery
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        if fishery.subsession.num_fish_at_start_of_year <= 0:
            yield Submission(views.Result, {}, check_html=False)
