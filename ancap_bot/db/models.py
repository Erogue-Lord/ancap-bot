from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    user_id = fields.BigIntField()
    balance = fields.DecimalField(10, 2, default=0)
    work = fields.DatetimeField(null=True, default=None)
