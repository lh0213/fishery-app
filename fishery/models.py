from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency
)


doc = """
Fishery app, etc.
"""


class Constants(BaseConstants):
    players_per_group = None
    num_rounds = 3
    name_in_url = 'fishery'

    instructions_template = 'fishery/Instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    two_thirds_avg = models.FloatField()
    best_guess = models.PositiveIntegerField()
    num_winners = models.PositiveIntegerField()

    def set_payoffs(self):
        pass


class Player(BasePlayer):
    username = models.CharField()
    fish_caught = models.PositiveIntegerField()
