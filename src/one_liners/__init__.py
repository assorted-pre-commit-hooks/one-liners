# SPDX-FileCopyrightText: 2026 Karl Wette
#
# SPDX-License-Identifier: MIT

"""Various one-liner pre-commit hooks."""

import argparse
from pathlib import Path
from typing import Sequence

import regex as re

__author__ = "Karl Wette"


class one_liner:
    """Base class for one-liners."""

    registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        one_liner.registry[cls.__name__] = cls


class regex(one_liner):
    """Regular expression search and replace."""

    def __init__(self, parser):
        parser.add_argument("--patt", type=str, required=True)
        parser.add_argument("--repl", type=str, required=True)

    def __call__(self, args, filepath):
        filepath.write_text(
            re.sub(args.patt, args.repl, filepath.read_text(), flags=re.MULTILINE)
        )


def main(argv: Sequence[str] | None = None) -> int:
    """Main function."""

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    subparsers.required = True
    for name in one_liner.registry:
        subparser = subparsers.add_parser(name)
        cls = one_liner.registry[name](subparser)
        subparser.add_argument("filenames", nargs="*")
        subparser.set_defaults(f=cls)

    args = parser.parse_args(argv)

    for filename in args.filenames:
        args.f(args, Path(filename))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
