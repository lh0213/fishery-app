from . import models
from ._builtin import Page, WaitPage


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class Catch(Page):
    form_model = models.Player
    form_fields = ['num_fish_caught_this_year']

    def vars_for_template(self):
        current_year = self.round_number

        # magic code!
        #if current_year > 1:
        #    self.subsession.num_fish_at_start = self.subsession.in_round(current_year - 1) \
        #            .num_fish_at_start

        #Is it correct?
        if current_year > 1:
            self.subsession.num_fish_left_this_year = self.subsession.in_round(current_year - 1) \
                    .num_fish_left_this_year

        return {
            'year_number': self.round_number + self.Constants.this_year,
            'num_fish_left_in_fishery': self.subsession.num_fish_left_this_year,
        }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        continue_game = self.group.set_payoffs()

class Results(Page):
    def vars_for_template(self):
        return {
            'num_total_fish_caught': self.participant.payoff,
            'num_fish_left_in_fishery': self.num_fish_left_this_year,
        }
    pass

page_sequence = [Introduction,
                 Catch,
                 ResultsWaitPage,
                 Results]
