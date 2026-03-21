# assorted-pre-commit-hooks / one-liners

Various one-liner [pre-commit] hooks.

## chmod

Change file permissions.

To use the hook, add the following to `.pre-commit-hooks.yaml`:

```
repos:
  - repo: https://github.com/assorted-pre-commit-hooks/one-liners
    rev: # see repository for latest tag
    hooks:
      - id: chmod
        args: [--{u|g|o}{R|W|X|r|w|x}, ...]
        files: # file include pattern
```

Each argument denotes a file permission to add or remove:

* `u`: user/owner permissions
* `g`: group permissions
* `o`: others permissions
* `R`: add read permission
* `W`: add read permission
* `X`: add execute permission
* `r`: remove read permission
* `w`: remove read permission
* `x`: remove execute permission

## regex

Regular expression search and replace.

To use the hook, add the following to `.pre-commit-hooks.yaml`:

```
repos:
  - repo: https://github.com/assorted-pre-commit-hooks/one-liners
    rev: # see repository for latest tag
    hooks:
      - id: regex
        args: [--patt, "...", --repl, "..."]
        files: # file include pattern
```

Search for the regular expression `--patt` in the included files; where found,
replace with `--repl`. Matching is performed line by line, e.g. `^` and `$`
match the start and end of each line respectively. Regular expressions are
compiled with [regex].

[pre-commit]:   https://pre-commit.com/
[regex]:        https://pypi.org/project/regex/
