from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):

        # yield SubmissionMustFail(views.Login, {'user_name': '', 'student_id': 'A0162533Q'})
        # yield SubmissionMustFail(views.Login, {'user_name': 'Liu Hang', 'student_id': ''})
        # yield SubmissionMustFail(views.Login, {'user_name': '', 'student_id': ''})

        # print("player id in group: " + self.player.id_in_group)
        username = 'Fan' * self.player.id_in_group
        student_id = 31415926 + self.player.id_in_group
        yield (views.Login, {'user_name': username, 'student_id': student_id})
        yield (views.Instructions)
