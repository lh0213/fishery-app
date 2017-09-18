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

page_sequence = [Login,
                 Instructions,
                ]
