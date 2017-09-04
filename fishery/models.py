from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency
)
import datetime

author = 'Fan Yuting & Liu Hang'
doc = """
Fishery app, etc.
"""


class Constants(BaseConstants):
    name_in_url = 'fishery'
    players_per_group = 3
    num_rounds = 3

    # Views
    instructions_template = 'fishery/Instructions.html'


class Subsession(BaseSubsession):
    # Record it here since we will need the value for each single year
    #? why two assignments to num_fish_at_start
    num_fish_at_start = models.PositiveIntegerField()
    this_year = datetime.datetime.year;

    def creating_session(self):
        self.num_fish_at_start = self.session.config['starting_fish_count']

    num_fish_left_this_year = num_fish_at_start


class Group(BaseGroup):
    def set_payoffs(self):
        # Need to decide whether to end game here if there are no more fish
        # Returns boolean: whether to continue the game
        for p in self.get_players():
            self.subsession.num_fish_left_this_year -= p.num_fish_caught_this_year
        if self.subsession.num_fish_left_this_year > 0:
            # Only give payoff if there are positive number of fish left
            for p in self.get_players():
                p.payoff = p.num_fish_caught_this_year
                p.total_fish_caught += p.num_fish_caught_this_year
            return True
        else:
            return False


class Player(BasePlayer):
    # Name may be duplicated, use student id as the key
    user_name = models.CharField()
    student_id = models.CharField()

    total_fish_caught = 0
    num_fish_caught_this_year = models.PositiveIntegerField(
        choices=[0, 1, 2],
        widget=widgets.RadioSelect()
    )

    #def role(self):
    #    if self.user_name == 'teacher' and self.student_id == '00000000':
    #        return 'Teacher'
    #    else:
    #        return 'Student'

    #Public void catchFish(int numOfFishCaughtThisYear);
