# Helper functions
import datetime


def display_year(page):
    current_year = page.round_number
    return current_year - 1 + datetime.date.today().year


def catch_fish_history(subsession):
    catch_history = []
    for sub in subsession.in_previous_rounds():
        catch_history.append(sub.num_fish_at_start_of_year)
    return catch_history


def catch_yield_history(subsession):
    catch_history = []
    for sub in subsession.in_previous_rounds():
        catch_history.append(sub.this_year_yield)
    return catch_history


def catch_sustainable_yield_history(subsession):
    catch_history = []
    for sub in subsession.in_previous_rounds():
        catch_history.append(sub.this_year_sustainable_yield)
    return catch_history
