from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency
)

author = 'Fan Yuting & Liu Hang'
doc = """
Fishery app, etc.
"""


class Constants(BaseConstants):
    name_in_url = 'fishery'
    players_per_group = None
    num_rounds = 100

    # Views
    instructions_template = 'fishery/Instructions.html'


class Subsession(BaseSubsession):
    # Record it here since we will need the value for each single year
    #? why two assignments to num_fish_at_start
    num_fish_at_start_of_year = models.PositiveIntegerField()

    def creating_session(self):
        self.num_fish_at_start_of_year = self.session.config['starting_fish_count']
        self.session.vars['continue_game'] = True # For ending the game early when there are no more fish

class Group(BaseGroup):
    def set_payoffs(self):
        # Need to decide whether to end game here if there are no more fish
        # Returns boolean: whether to continue the game
        # Using variable names as used in the Beverton-Holt model
        # (h)arvest: H, total number of fish caught in the round
        # n_t: number of fsh at start of year
        # (r)ate: r, intrinsic growth rate
        # a: strength of density regulation
        harvest = 0
        n_t = self.subsession.num_fish_at_start_of_year
        rate = self.session.config['intrinsic_growth_rate']
        a = self.session.config['strength_of_density_regulation']
        num_fish_for_next_year = 0

        for p in self.get_players():
            harvest += p.num_fish_caught_this_year

        # Applying the formula here
        num_fish_for_next_year = ((1 + rate) * n_t) / (1 + a * n_t) - harvest
        if num_fish_for_next_year > 0:
            # Store the result and pass to the next round later
            self.subsession.num_fish_at_start_of_year = num_fish_for_next_year

            # Only give payoff if there are positive number of fish left
            for p in self.get_players():
                p.payoff = p.num_fish_caught_this_year

            return True
        else:
            return False


class Player(BasePlayer):
    # Name may be duplicated, use student id as the key
    user_name = models.CharField()
    student_id = models.CharField()

    #total_fish_caught = 0
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
