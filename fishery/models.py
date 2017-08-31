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
    # Record it here since we will need the value for each single year
    num_fish_at_start = models.PositiveIntegerField()

    def creating_session(self):
        self.num_fish_at_start = self.session.config['starting_fish_count']


class Group(BaseGroup):
    def set_payoffs(self):
        # Need to decide whether to end game here if there are no more fish
        # Returns boolean: whether to continue the game
        for p in self.get_players():
            self.subsession.num_fish_at_start -= p.num_fish_caught_this_year
        if self.subsession.num_fish_at_start > 0:
            # Only give payoff if there are positive number of fish left
            for p in self.get_players():
                p.payoff = p.num_fish_caught_this_year
            return True
        else:
            return False

class Player(BasePlayer):
    username = models.CharField()
    num_fish_caught_this_year = models.PositiveIntegerField()

    # Not sure whether we really need these fields
    #student_id = models.CharField()

    #Public void catchFish(int numOfFishCaughtThisYear);
