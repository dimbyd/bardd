# settings.py

import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_ROOT = os.path.join(PROJECT_ROOT, 'cronfa')
LOG_ROOT = os.path.join(PROJECT_ROOT, 'logs')

#-----------------------------------------

LOG_FILE_NAME = os.path.join(LOG_ROOT, 'bardd.log')

ADMINS = (
    ('scmde', 'evansd8@caerdydd.ac.uk'),
)

DATABASES = {
    'default': {
        'ODLAU': os.path.join(DATA_ROOT, 'static/odliadurRS.json'),
        'GEIRFA': os.path.join(DATA_ROOT, 'static/geiriauJGJ.txt'),
    }
}


# print(PROJECT_ROOT)
# print(SRC_ROOT)
# print(DATA_ROOT)
