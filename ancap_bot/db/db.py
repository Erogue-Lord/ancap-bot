from decimal import Decimal
from typing import Optional

from tortoise import Tortoise

from .. import settings, exceptions
from . import models


async def transaction(user_id: int, amount: Decimal, target_id: Optional[int] = None):
    user = await models.User.filter(user_id=user_id).first()
    if user is None:
        raise exceptions.NonexistentUserError(
            _("You're not registered, use $init to create your bank acount")
        )
    if user.balance >= amount:
        if target_id is not None:
            target = await models.User.filter(user_id=target_id).first()
            if target is not None:
                target.balance += amount
                await target.save()
            else:
                raise exceptions.NonexistentUserError(_("Non-existent user"))
        user.balance -= amount
        await user.save()
    else:
        raise exceptions.InsufficientFundsError(_("You don't have that money"))


async def init():
    await Tortoise.init(
                db_url=f'{settings.DB}',
                modules={'models': ['ancap_bot.db.models']}
            )
    await Tortoise.generate_schemas()
