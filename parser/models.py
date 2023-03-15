from peewee import *

db = SqliteDatabase('database/tasks.db')


class BaseModel(Model):
    id = PrimaryKeyField()

    class Meta:
        database = db


class Tag(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'tags'


class Task(BaseModel):
    id = CharField(unique=True)
    name = CharField()
    tags = ManyToManyField(
        Tag
    )
    complexity = IntegerField()
    solution = CharField()

    class Meta:
        db_table = 'tasks'
        order_by = 'complexity'
