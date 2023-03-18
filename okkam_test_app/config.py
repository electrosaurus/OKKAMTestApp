''' App configuration variables. '''

import os


db_host = os.getenv('OKKAM_TEST_APP_DB_HOST', 'localhost')
db_name = os.getenv('OKKAM_TEST_APP_DB_NAME', 'okkam')
db_user = os.getenv('OKKAM_TEST_APP_DB_USER', 'okkam')
db_user_password = os.getenv('OKKAM_TEST_APP_DB_USER_PASSWORD', 'okkam')
