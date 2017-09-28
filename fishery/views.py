from . import models
from . import utils
from ._builtin import Page, WaitPage

class TeacherStartPage(Page):
    # def is_displayed(self):
    # display when player.role = "teacher"
    form_model = models.Constants
    form_fields = ['para_intrinsic_growth_rate','para_strength_of_density_regulation',
                   'para_sustainable_yield','para_total_num_of_fish']


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

    def is_displayed(self):
        return self.session.vars['continue_game']

    def vars_for_template(self):
        if self.round_number > 1:
            self.subsession.num_fish_at_start_of_year = self.subsession.in_round(self.round_number - 1) \
                    .num_fish_at_start_of_year

        return {
            "year_number": utils.display_year(self),
            "catch_history": utils.catch_history(self.subsession),
            # 'year_number': self.round_number + self.subsession.this_year,
            'num_fish_left_in_fishery': self.subsession.num_fish_at_start_of_year,
            # Constants
            "intrinsic_growth_rate": self.session.config['intrinsic_growth_rate'],
            "strength_of_density_regulation": self.session.config['strength_of_density_regulation'],
            "sustainable_yield": self.session.config['sustainable_yield'],
            "player_name": self.participant.vars['name'],
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