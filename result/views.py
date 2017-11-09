from . import models
from . import utils
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Result(Page):

    def vars_for_template(self):
        participant = self.participant
        return {
            # Graph Variables
            "each_year_fish_history": self.session.vars['fish_history'],
            "each_year_yield_history": self.session.vars['yield_history'],
            "each_year_sustainable_yield_history": self.session.vars['sustainable_yield_history'],
        }

page_sequence = [Result]
