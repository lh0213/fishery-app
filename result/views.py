from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Result(Page):

    def vars_for_template(self):
        participant = self.participant

page_sequence = [Result]
