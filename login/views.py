from . import models
from ._builtin import Page, WaitPage
import math


class Login(Page):
    form_model = models.Player
    form_fields = ['user_name', 'student_id']


class Instructions(Page):

    def before_next_page(self):
        self.participant.vars['name'] = self.player.user_name
        self.participant.vars['id'] = self.player.student_id

    def vars_for_template(self):
        rate = self.session.config['intrinsic_growth_rate']
        n_t = self.session.config['starting_fish_count']
        a = self.session.config['strength_of_density_regulation']

        year_sustainable_yield = ((1 + rate) * n_t) / (1 + a * n_t) - n_t
        return {
                # Constants
                "intrinsic_growth_rate": rate,
                "strength_of_density_regulation": a,
                "total_fish": n_t,
                "sustainable_yield": math.ceil(year_sustainable_yield*1000)/1000
        }

page_sequence = [Login,
                 Instructions,
                ]
