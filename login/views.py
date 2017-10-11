from . import models
from ._builtin import Page, WaitPage
import datetime


class Login(Page):
    form_model = models.Player
    form_fields = ['user_name', 'student_id']


class Instructions(Page):
    def before_next_page(self):
        self.participant.vars['name'] = self.player.user_name
        self.participant.vars['id'] = self.player.student_id

    def vars_for_template(self):
        return {
                # Constants
                "intrinsic_growth_rate": self.session.config['intrinsic_growth_rate'],
                "strength_of_density_regulation": self.session.config['strength_of_density_regulation'],
                "sustainable_yield": self.session.config['sustainable_yield'],
                "total_fish": self.session.config['starting_fish_count']
        }

page_sequence = [Login,
                 Instructions,
                ]
