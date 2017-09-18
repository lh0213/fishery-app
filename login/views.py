from . import models
from ._builtin import Page, WaitPage
import datetime


class Login(Page):
    form_model = models.Player
    form_fields = ['user_name', 'student_id']


class Instructions(Page):
    pass

page_sequence = [Login,
                 Instructions,
                ]
