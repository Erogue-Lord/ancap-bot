class AncapBotError(Exception):
    pass


class InsufficientFundsError(AncapBotError):
    pass


class NonexistentUserError(AncapBotError):
    pass
