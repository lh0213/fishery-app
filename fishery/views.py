from . import models
from ._builtin import Page, WaitPage
import datetime


class Login(Page):
    form_model = models.Player
    form_fields = ['user_name', 'student_id']


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


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


class TeacherFinalResult(Page):
    # def is_displayed(self):
    # when to display?
    def vars_for_template(self):
        return {
            'num_fish_left_in_fishery': self.subsession.num_fish_at_start_of_year,
        }


class StudentCatch(Page):
    form_model = models.Player
    form_fields = ['num_fish_caught_this_year']

    def vars_for_template(self):
        current_year = self.round_number
        display_year = current_year - 1 + datetime.date.today().year

        if current_year > 1:
            self.subsession.num_fish_at_start_of_year = self.subsession.in_round(current_year - 1) \
                    .num_fish_at_start_of_year

        return {
            'year_number': display_year,
            # 'year_number': self.round_number + self.subsession.this_year,
            'num_fish_left_in_fishery': self.subsession.num_fish_at_start_of_year,
            'para_r': self.Constants.para_intrinsic_growth_rate,
            'para_a': self.Constants.para_strength_of_density_regulation,
            'para_hmax': self.Constants.para_sustainable_yield,
            'total_fish_till_this_round': self.participant.payoff
        }


class OutOfFishResult(Page):
    def is_displayed(self):
        return self.subsession.num_fish_at_start_of_year < 0

    def vars_for_template(self):
        return {
            'num_total_fish_caught': self.participant.payoff,
        }


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        continue_game = self.group.set_payoffs()


class StudentFinalResult(Page):
    def vars_for_template(self):
        return {
            'num_total_fish_caught': self.participant.payoff,
            'num_fish_left_in_fishery': self.subsession.num_fish_at_start_of_year,
        }

page_sequence = [Login,
                 Instructions,
                 TeacherStartPage,
                 StudentCatch,
                 ResultsWaitPage,
                 TeacherEachYearResult,
                 OutOfFishResult,
                 StudentFinalResult]
