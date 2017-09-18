from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency
)

author = 'Fan Yuting & Liu Hang'
doc = """
Fishery app, etc.
"""


class Constants(BaseConstants):
    name_in_url = 'login'
    players_per_group = None
    num_rounds = 1

    # Views
    instructions_template = 'login/Instructions.html'


class Subsession(BaseSubsession):

    def creating_session(self):
        pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Name may be duplicated, use student id as the key
    user_name = models.CharField()
    student_id = models.CharField()
