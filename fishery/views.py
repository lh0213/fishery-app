from . import models
from . import utils
from ._builtin import Page, WaitPage
import math

class TeacherStartPage(Page):
    # def is_displayed(self):
    # display when player.role = "teacher"
    form_model = models.Constants
    form_fields = ['para_intrinsic_growth_rate','para_strength_of_density_regulation',
                   'para_total_num_of_fish']


class TeacherEachYearResult(Page):
    # def is_displayed(self):
    # when to display?
    def vars_for_template(self):
        return {
            'num_fish_left_in_fishery': self.subsession.num_fish_at_start_of_year,
        }
# displaying the same chart in the admin report and participant pages


class TeacherFinalResult(Page):
    # def is_displayed(self):
    # when to display?

    # displays the same chart in the admin report and participant pages
    def vars_for_template(self):
        vars_dict = {
            'num_fish_left_in_fishery': self.subsession.num_fish_at_start_of_year,
        }
        vars_dict.update(self.subsession.vars_for_admin_report())
        return vars_dict


class StudentCatch(Page):
    form_model = models.Player
    form_fields = ['num_fish_caught_this_year']
    ##timeout_seconds = 30

    def is_displayed(self):
        return self.session.vars['continue_game']

    def vars_for_template(self):
        if self.round_number == 1:
            rate = self.session.config['intrinsic_growth_rate']
            n_t = self.session.config['starting_fish_count']
            a = self.session.config['strength_of_density_regulation']
            year_sustainable_yield = ((1 + rate) * n_t) / (1 + a * n_t) - n_t

        if self.round_number > 1:
            self.subsession.num_fish_at_start_of_year = self.subsession.in_round(self.round_number - 1) \
                .num_fish_at_start_of_year

            self.subsession.this_year_sustainable_yield = self.subsession.in_round(self.round_number - 1) \
                .this_year_sustainable_yield

            self.subsession.this_year_yield = self.subsession.in_round(self.round_number - 1) \
                .this_year_yield

            year_sustainable_yield = self.subsession.this_year_sustainable_yield


        return {
            "year_number": utils.display_year(self),
            "player_name": self.participant.vars['name'],

            # Graph Variables
            "each_year_fish_history": utils.catch_fish_history(self.subsession),
            "each_year_yield_history": utils.catch_yield_history(self.subsession),
            "each_year_sustainable_yield_history": utils.catch_sustainable_yield_history(self.subsession),

            # Table Variables
            'num_fish_left_in_fishery': self.subsession.num_fish_at_start_of_year,
            "sustainable_yield": math.ceil(year_sustainable_yield * 1000)/1000,

            # Table Constants
            "intrinsic_growth_rate": self.session.config['intrinsic_growth_rate'],
            "strength_of_density_regulation": self.session.config['strength_of_density_regulation'],
        }


class OutOfFishResult(Page):
    def is_displayed(self):
        return self.subsession.num_fish_at_start_of_year < 0

    def vars_for_template(self):
        return {
            'num_total_fish_caught': self.participant.payoff,
        }


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.session.vars['continue_game']

    def after_all_players_arrive(self):
        self.session.vars['continue_game']= self.group.set_payoffs()


class StudentFinalResult(Page):
    timeout_seconds = 5
    def is_displayed(self):
        return self.session.vars['continue_game']

    def vars_for_template(self):
        return {
            'num_total_fish_caught': self.participant.payoff,
            'num_fish_left_in_fishery': self.subsession.num_fish_at_start_of_year,
            'year_number': utils.display_year(self),
        }

page_sequence = [StudentCatch,
                 ResultsWaitPage,
                 #TeacherEachYearResult,
                 # OutOfFishResult,
                 StudentFinalResult]
                 #TeacherFinalResult]
