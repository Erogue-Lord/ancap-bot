import sys
from textwrap import dedent

from . import AncapBot
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
            AncapBot()
        elif arg == "updatedb":
            updatedb()
        else:
            print(_("type --help for the options"))


if __name__ == "__main__":
    main_cli()
