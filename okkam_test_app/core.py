''' General objects used on the application level. '''

import psycopg2

from audience_calculator import AudienceCalculator
from config import db_host, db_name, db_user, db_user_password


db_session = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_user_password,
)
audience_calculator = AudienceCalculator(db_session)
