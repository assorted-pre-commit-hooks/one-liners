# SPDX-FileCopyrightText: 2026 Karl Wette
#
# SPDX-License-Identifier: MIT

"""Test one-liners."""

import stat

import pytest

from one_liners import main


@pytest.mark.parametrize(
    "opt, f",
    [
        # --- owner ---
        ("--uR", stat.S_IRUSR),
        ("--uW", stat.S_IWUSR),
        ("--uX", stat.S_IXUSR),
        # --- group ---
        ("--gR", stat.S_IRGRP),
        ("--gW", stat.S_IWGRP),
        ("--gX", stat.S_IXGRP),
        # --- other ---
        ("--oR", stat.S_IROTH),
        ("--oW", stat.S_IWOTH),
        ("--oX", stat.S_IXOTH),
    ],
)
def test_chmod_addf(tmp_path, opt, f):
    """Test chmod adding permissions."""

    tmp_file = tmp_path / "chmod.dat"
    tmp_file.write_text(":")

    tmp_file.chmod(0)
    assert stat.S_IMODE(tmp_file.stat().st_mode) == 0

    main(["chmod", opt, str(tmp_file)])

    assert stat.S_IMODE(tmp_file.stat().st_mode) == f


@pytest.mark.parametrize(
    "opt, f",
    [
        # --- owner ---
        ("--ur", stat.S_IRUSR),
        ("--uw", stat.S_IWUSR),
        ("--ux", stat.S_IXUSR),
        # --- group ---
        ("--gr", stat.S_IRGRP),
        ("--gw", stat.S_IWGRP),
        ("--gx", stat.S_IXGRP),
        # --- other ---
        ("--or", stat.S_IROTH),
        ("--ow", stat.S_IWOTH),
        ("--ox", stat.S_IXOTH),
    ],
)
def test_chmod_subf(tmp_path, opt, f):
    """Test chmod removing permissions."""

    tmp_file = tmp_path / "chmod.dat"
    tmp_file.write_text(":")

    tmp_file.chmod(0o777)
    assert stat.S_IMODE(tmp_file.stat().st_mode) == 0o777

    main(["chmod", opt, str(tmp_file)])

    assert stat.S_IMODE(tmp_file.stat().st_mode) == 0o777 & ~f


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
