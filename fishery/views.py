from fishery.models import Constants
from . import models
from . import utils
from ._builtin import Page, WaitPage
import math, random


class StudentCatch(Page):
    form_model = models.Player
    form_fields = ['num_fish_caught_this_year']
    # timeout_seconds = 30        # if time limit is needed, then uncomment this line.

    # Game: Awards for Upgrading
    # Replaces numbers with rewards for each level
    rewards_list = ["level 0", "level 1",
         "You bought and planted a palm tree",  #level 2
         "You bought a house",                  #level 3
         "The weather is great",                #level 4
         "You bought some flowers",             #level 5
         "You planted a flower farm",           #level 6
         "You built a fence for your farm",     #level 7
         "You made a scarecrow",                #level 8
         "You bought a mailbox",                #level 9
         "You built a chicken coop",            #level 10
         "You bought a cat",                    #level 11
         "You bought a puppy",                  #level 12
         "You discovered some rare rocks",      #level 13
         "You discovered some sea creatures",   #level 14
         "You bought some sea stars and sea shells",                  #level 15
         "You bought a llama",                  #level 16
         "You trained some seabirds",           #level 17
         "You caught a clown fish",             #level 18
         "You bought a sailboat",               #level 19
         "You befriended some pet seafish",     #level 20
         "You befriended a dolphin",            #level 21
         "A rainbow appeared. You dug at the other end of the rainbow and discovered" +
         "a treasure box. You are now a millionaire" #level 22
    ]

    def is_displayed(self):
        return self.session.vars['continue_game']

    def vars_for_template(self):
        is_upgrade = False
        last_year_catch = 0
        cutoff = 0
        rad = 0

        if self.round_number <= 1:
            # Initializes the parameters
            rate = self.session.config['intrinsic_growth_rate']
            n_t = self.session.config['starting_fish_count']
            a = self.session.config['strength_of_density_regulation']
            year_sustainable_yield = ((1 + rate) * n_t) / (1 + a * n_t) - n_t

            # Game level information
            url_pic = "global/1.jpg"
            self.participant.vars['game_level'] = 1
            self.participant.vars['next_upgrade_fish_count'] = 0

        if self.round_number > 1:
            # Updates data for the upcoming year

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


            # Gamification design

            # Default upgrade interval is 5
            # As level gets higher, there is a lower chance that the upgrade will actually
            # take place
            last_year_catch = self.player.in_round(self.round_number - 1).payoff
            self.participant.vars['next_upgrade_fish_count'] += last_year_catch

            exp = self.participant.vars['next_upgrade_fish_count'] # experience point needed to upgrade

            if (exp > 5):
                n = self.participant.vars['game_level']
                cutoff = math.log(n + 15, 16) * (n ** (-3/4)) * math.log(exp, 5)
                rad = random.random()

                if (rad <= cutoff):
                    is_upgrade = True
                    self.participant.vars['game_level'] += 1
                    self.participant.vars['next_upgrade_fish_count'] = 0

        game_level = self.participant.vars['game_level']

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
            'exp': self.participant.vars['next_upgrade_fish_count'],
            'cutoff': cutoff,
            'rad': rad,

            # Graph Variables
            "each_year_fish_history": utils.catch_fish_history(self.subsession),
            "each_year_yield_history": utils.catch_yield_history(self.subsession),
            "each_year_sustainable_yield_history": utils.catch_sustainable_yield_history(self.subsession),

            # debug info
            "critical_value": self.subsession.sustainable_yield_critical_value,

            # Table Variables
            'num_fish_left_in_fishery': self.subsession.num_fish_at_start_of_year,
            "sustainable_yield": math.ceil(year_sustainable_yield * 1000)/1000,

            # Gamificatioin
            'game_level': game_level,
            'level_reward': self.rewards_list[game_level] if (game_level <= 20) else "a surpise",
            'is_upgrade' : is_upgrade,

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
                 StudentFinalResult]
