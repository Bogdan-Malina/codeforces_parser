import os
from dotenv import load_dotenv
from peewee import *

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

db = PostgresqlDatabase(
    database=DB_NAME,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)


class BaseModel(Model):
    id = PrimaryKeyField()

    class Meta:
        database = db


class Tag(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'tags'


class Complexity(BaseModel):
    name = CharField(unique=True)

    class Meta:
        order_by = 'name'
        db_table = 'complexity'


class Task(BaseModel):
    task_id = CharField(unique=True)
    name = CharField()
    tags = ManyToManyField(
        Tag,
        backref='tasks'
    )
    complexity = ForeignKeyField(
        Complexity
    )
    solution = CharField()

    class Meta:
        db_table = 'tasks'
        order_by = 'complexity'
