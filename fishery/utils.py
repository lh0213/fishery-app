# Helper functions
import datetime

def display_year(page):
    current_year = page.round_number
    return current_year - 1 + datetime.date.today().year
