import sys
from textwrap import dedent

from . import AncapBot, settings
from .db import updatedb


def main_cli():  # TODO: use argparse and add error handling
    if len(sys.argv) <= 1:
        print(_("type --help for the options"))
    else:
        arg = sys.argv[1]
        if arg == "--help" or arg == "-h":
            print(
                dedent(
                    _(
                        """\
                ancap-bot CLI Options:
                run:
                    run the bot
                updatedb:
                    populate de database with tables
                """
                    )
                )
            )
        elif arg == "run":
            if settings.DB == "sqlite:///:memory:":
                updatedb()
            AncapBot()
        elif arg == "updatedb":
            updatedb()
        else:
            print(_("type --help for the options"))
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main_cli())
