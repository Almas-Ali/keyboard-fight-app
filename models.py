from peewee import *
from datetime import datetime

db = SqliteDatabase('sqlite.db')


class BaseModel(Model):
    class Meta:
        database = db


class Contest(BaseModel):
    full_name = CharField(default='', max_length=50)  # John Doe
    roll_no = IntegerField(default=0)               # 421245
    section = CharField(default='', max_length=50)  # 2022-23
    shift = CharField(default='', max_length=50)    # 1st / 2nd

    unique_id = CharField(default='', max_length=50)  # 421245-2022-23-1st
    response = TextField(default='')  # Submitted response data

    word_count = IntegerField(default=0)  # Word count of the response

    # Timestamp of submission
    timestamp = DateTimeField(default=datetime.now())

    class Meta:
        db_table = 'contest'
