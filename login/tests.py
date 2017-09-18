from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    @staticmethod
    def play_round(self):
        yield (views.Introduction)

        yield SubmissionMustFail(views.Login, {'user_name': '', 'student_id': 'A0162533Q'})
        yield SubmissionMustFail(views.Login, {'user_name': 'Liu Hang', 'student_id': ''})
        yield SubmissionMustFail(views.Login, {'user_name': '', 'student_id': ''})

        for i in range(1, 60):
            username = 'Fan' * i
            student_id = 31415926 + i

            yield (views.Login, {'user_name': username, 'student_id': student_id})

