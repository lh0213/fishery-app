import os
from os import environ

import dj_database_url

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

# don't share this with anybody.
SECRET_KEY = 'bumowj_64kq5p9ta*1)r2l(lk2hl2hfb@8=_^*zryjmjeeth*k'


DATABASES = {
    'default': dj_database_url.config(
        # Rather than hardcoding the DB parameters here,
        # it's recommended to set the DATABASE_URL environment variable.
        # This will allow you to use SQLite locally, and postgres/mysql
        # on the server
        # Examples:
        # export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
        # export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME

        # fall back to SQLite if the DATABASE_URL env var is missing
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
USE_POINTS = True
POINTS_CUSTOM_NAME = 'fish'



# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            oTree on GitHub
        </a>.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Here are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish.
</p>
"""

ROOMS = [
    {
        'name': 'lsm4255',
        'display_name': 'LSM4255',
        #'use_secure_urls': True
        #'participant_label_file': '_rooms/students.txt',
    }
]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.00,
    'real_world_currency_code': 'fish',
    'participation_fee': 0.00,
    'real_world_currency_decimal_places': 0,
    'doc': "",
}

SESSION_CONFIGS = [
     {
        'name': 'fishery',
        'display_name': 'Fishery Simulator',
        'num_demo_participants': 3,
        'app_sequence': ['login', 'fishery', 'result'],
        # Default values for parameters, from the demo ppt
        'intrinsic_growth_rate': 0.4,
        'strength_of_density_regulation': 0.001,
        'sustainable_yield': 40.5,
        # Round to a nicer number because why not
        'starting_fish_count': 10,
        'use_browser_bots': True
    },
]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
