import sys
from textwrap import dedent

from .bot import AncapBot


def main_cli():  # TODO: use argparse and add error handling
    if len(sys.argv) <= 1:
        print(_("type --help for the options"))
        return 1
    else:
        arg = sys.argv[1]
        if arg in {"--help", "-h"}:
            print(
                dedent(
                    _(
                        """\
                ancap-bot CLI Options:
                run:
                    run the bot
                --help -h:
                    shows this message
                """
                    )
                )
            )
        elif arg == "run":
            AncapBot()
        else:
            print(_("type --help for the options"))
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main_cli())
