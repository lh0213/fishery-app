from fishery.models import Constants
from . import models
from . import utils
from ._builtin import Page, WaitPage
import math


class StudentCatch(Page):
    form_model = models.Player
    form_fields = ['num_fish_caught_this_year']

    timeout_seconds = 30

    def is_displayed(self):
        return self.session.vars['continue_game']

    def vars_for_template(self):
        if self.round_number <= 1:
            rate = self.session.config['intrinsic_growth_rate']
            n_t = self.session.config['starting_fish_count']
            a = self.session.config['strength_of_density_regulation']
            year_sustainable_yield = ((1 + rate) * n_t) / (1 + a * n_t) - n_t

            #game
            url_pic = "global/1.jpg"
            self.player.game_level = 1
            self.player.next_upgrade_fish_count = 2

        if self.round_number > 1:
            self.subsession.num_fish_at_start_of_year = self.subsession.in_round(self.round_number - 1) \
                .num_fish_at_start_of_year

            self.subsession.this_year_sustainable_yield = self.subsession.in_round(self.round_number - 1) \
                .this_year_sustainable_yield

            self.subsession.this_year_yield = self.subsession.in_round(self.round_number - 1) \
                .this_year_yield

            self.subsession.this_year_harvest = self.subsession.in_round(self.round_number - 1) \
                .this_year_harvest
            self.subsession.total_harvest = self.subsession.in_round(self.round_number - 1) \
                .total_harvest
            self.subsession.numPlayers = self.subsession.in_round(self.round_number - 1) \
                .numPlayers
            self.subsession.this_year_average_yield = self.subsession.in_round(self.round_number - 1) \
                .this_year_average_yield
            self.subsession.total_average_yield = self.subsession.in_round(self.round_number - 1) \
                .total_average_yield
            year_sustainable_yield = self.subsession.this_year_sustainable_yield


            # gamification design

            #if self.participant.payoff > self.player.next_upgrade_fish_count \
            #        and self.player.game_level <= 10:
              #  self.player.game_level += 1
              #  self.player.next_upgrade_fish_count += 2
            self.player.game_level = int(math.ceil(int(self.participant.payoff) / 5));
                #while self.player.next_upgrade_fish_count < self.participant.payoff:
                    #self.player.next_upgrade_fish_count += math.ceil(self.subsession.num_fish_at_start_of_year / numPlayers)
                    #self.player.next_upgrade_fish_count += 1



        return {
            "year_number": utils.display_year(self),
            "player_name": self.participant.vars['name'],

            # choice back variables
            "last_year_average_student_caught": math.ceil(self.subsession.this_year_average_yield*100)/100,
            "total_average_student_caught": math.ceil(self.subsession.total_average_yield*100)/100,

            # debug info
            "numPlayer": self.subsession.numPlayers,
            "numPlayer2": len(self.subsession.get_players()),
            'this_year_harvest': self.subsession.this_year_harvest,
            'total_harvest': self.subsession.total_harvest,

            # Graph Variables
            "each_year_fish_history": utils.catch_fish_history(self.subsession),
            "each_year_yield_history": utils.catch_yield_history(self.subsession),
            "each_year_sustainable_yield_history": utils.catch_sustainable_yield_history(self.subsession),

            # Table Variables
            'num_fish_left_in_fishery': self.subsession.num_fish_at_start_of_year,
            "sustainable_yield": math.ceil(year_sustainable_yield * 1000)/1000,

            # Game Picture Path
            #'upgrade_distance':int(math.ceil(int(self.participant.payoff) / 10)) - self.participant.payoff,
            'game_level': self.player.game_level,

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
                 # OutOfFishResult,
                 StudentFinalResult]
