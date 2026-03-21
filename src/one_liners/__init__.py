# SPDX-FileCopyrightText: 2026 Karl Wette
#
# SPDX-License-Identifier: MIT

"""Various one-liner pre-commit hooks."""

import argparse
import stat
from functools import partial, reduce
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


class chmod(one_liner):
    """Change file permissions."""

    @staticmethod
    def addf(m, f):
        return m | f

    @staticmethod
    def subf(m, f):
        return m & ~f

    def __init__(self, parser):
        for opt, modef, f in (
            # --- owner ---
            ("--uR", chmod.addf, stat.S_IRUSR),
            ("--uW", chmod.addf, stat.S_IWUSR),
            ("--uX", chmod.addf, stat.S_IXUSR),
            ("--ur", chmod.subf, stat.S_IRUSR),
            ("--uw", chmod.subf, stat.S_IWUSR),
            ("--ux", chmod.subf, stat.S_IXUSR),
            # --- group ---
            ("--gR", chmod.addf, stat.S_IRGRP),
            ("--gW", chmod.addf, stat.S_IWGRP),
            ("--gX", chmod.addf, stat.S_IXGRP),
            ("--gr", chmod.subf, stat.S_IRGRP),
            ("--gw", chmod.subf, stat.S_IWGRP),
            ("--gx", chmod.subf, stat.S_IXGRP),
            # --- other ---
            ("--oR", chmod.addf, stat.S_IROTH),
            ("--oW", chmod.addf, stat.S_IWOTH),
            ("--oX", chmod.addf, stat.S_IXOTH),
            ("--or", chmod.subf, stat.S_IROTH),
            ("--ow", chmod.subf, stat.S_IWOTH),
            ("--ox", chmod.subf, stat.S_IXOTH),
        ):
            parser.add_argument(
                opt, dest="perms", action="append_const", const=partial(modef, f=f)
            )

    def __call__(self, args, filepath):
        old_mode = filepath.stat().st_mode
        new_mode = reduce(lambda m, modef: modef(m), [old_mode] + args.perms)
        if old_mode != new_mode:
            filepath.chmod(new_mode)
            return 1
        return 0


class regex(one_liner):
    """Regular expression search and replace."""

    def __init__(self, parser):
        parser.add_argument("--patt", type=str, required=True)
        parser.add_argument("--repl", type=str, required=True)

    def __call__(self, args, filepath):
        old_text = filepath.read_text()
        new_text = re.sub(args.patt, args.repl, old_text, flags=re.MULTILINE)
        if old_text != new_text:
            filepath.write_text(new_text)
            return 1
        return 0


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

    exit_code = 0
    for filename in args.filenames:
        exit_code |= args.f(args, Path(filename))

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
