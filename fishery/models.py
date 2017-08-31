from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency
)


doc = """
Fishery app, etc.
"""


class Constants(BaseConstants):
    name_in_url = 'fishery'
    players_per_group = None
    num_rounds = 3

    # Views
    instructions_template = 'fishery/Instructions.html'


class Subsession(BaseSubsession):
    num_fish_at_start = models.PositiveIntegerField


class Group(BaseGroup):
    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = p.num_fish_caught_this_year

class Player(BasePlayer):
    username = models.CharField()
    num_fish_caught_this_year = models.PositiveIntegerField()

    # Not sure whether we really need these fields
    #student_id = models.CharField()

    #Public void catchFish(int numOfFishCaughtThisYear);
