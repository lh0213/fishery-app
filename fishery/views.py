from . import models
from ._builtin import Page, WaitPage


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class Catch(Page):
    form_model = models.Player
    form_fields = ['num_fish_caught']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    total_num_of_fish = 3030


page_sequence = [Introduction,
                 Catch,
                 ResultsWaitPage,
                 Results]
