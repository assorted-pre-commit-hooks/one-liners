# SPDX-FileCopyrightText: 2026 Karl Wette
#
# SPDX-License-Identifier: MIT

"""Test one-liners."""

from one_liners import main


def test_regex(tmp_path):
    """Test regex."""

    tmp_file = tmp_path / "regex.txt"
    with tmp_file.open("w") as f:
        print("   This line should not be indented", file=f)
        print("               Nor should this line", file=f)

    main(["regex", "--patt", "^ *", "--repl", "", str(tmp_file)])

    with tmp_file.open("r") as f:
        for line in f:
            assert line.strip() == line.rstrip()
