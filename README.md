# Faint Comments

This repository is my attempt in [100 commits competition](https://100commitow.pl/).

> :warning: This project is in PoC and still needs to be polished. Always pin version.
> Do backup or use version control before applying any command.

## What it is?

This library keeps your code comments in separate file and allows to put them back on.

## Why

Comments are [code smell](https://refactoring.guru/pl/smells/comments). But sometimes:

- you just want to have your own note that should never appear in Version Control.
- you have code that needs some comments but comments must always be removed before deploy on production.
- you want to give someone instruction on what to do in certain files.

In all this cases it would be handy to keep all comments
in separate file that could be potentially _git ignored_
but at the same time applied whenever you want to read them.

Also I thought I can learn some cool algorithms and tools.

---

## Demo

Imagine you have your code:

```python
# TODO: this name must be changed
def foo():
    ...
    i  = 0x5f3759df - ( i >> 1 ) # what the quack?
    ...
```

and maybe you do not think it is good to keep your comments in code.  
You run `faint extract <name_of_the_file>.py` as a result you get:

```python
def foo():
    ...
    i  = 0x5f3759df - ( i >> 1 )
    ...

```

and `JSON` file:

```json
{
  "comments": [
    {
      "start": {
        "row": 4,
        "column": 33
      },
      "text": "# what the quack?",
      "is_inline": true
    },
    {
      "start": {
        "row": 1,
        "column": 0
      },
      "text": "# TODO: this name must be changed",
      "is_inline": false
    }
  ],
  "deleted_lines": [1],
  "file_metadata": {
    "commit_sha": "sha_of_commit",
    "file_name": "path/to/file/<name_of_the_file>.py",
    "file_sha": "hash_of_the_file"
  }
}
```

and this file is kept as `comment_<name_of_the_file>.json`.  
At any moment you can `faint join <name_of_the_file>.py` and you will get original file.

But this tool also tries to handle situation when you will modify the file before `join` command and more.

## How to install

You can `pip` install:

```bash
pip3 install faint
```

## How to use

You can check what is available via `faint --help` or just `faint`.

`faint` is made of two main subcommands:

- `faint extract <file name>` which removes comments from code and place them in separate `JSON` file.
- `faint join <file name>` which applies comments from `JSON` file (if exists) in corresponding places.

By default (not changeable yet) `JSON` files are named as `comments_<original name>.json`.
So you can add to `.gitignore` line like `comments_*.json`.

### Workflow

First use `extract` on the file. Then you can:

- Use `join` and not modify the file
- Use `join` and modify the file
- Continue to modify the file and then use `join`

Then:

- If you apply `join` on file that matches exactly the file after `extract`
  it should be fast and simple and you should get all comments back in place.
- If you apply `join` and file follows the structure good enough you should also
  get all comments back in right place.

In both cases the `extract` should work as at the beginning.

Current version does not allow for:

- `extract` on already `extract`ed file (it will discard all comments in `JSON`)
- `join` on already `join`ed file (it will place the comments twice)

So if you want to add any new comments you should first `join` comments and the extract them.

## Supported languages

This tool uses `TreeSitter`. For every language the `AST` (Abstract Syntax Tree) has different nodes.
For this reason every language needs to be covered separately.

- [x] Python

## Tests

This tool will have many edge cases to cover. The tests for now does not need to pass any treshold, but are more a track of edge cases to cover in future.

## TODO

- [x] Make it pip installable
- [ ] Fix double join
- [ ] When extracting, compare with current `JSON`
- [ ] Show abandoned comments
- [ ] Show deleted comments
- [ ] When `join` and comment is abandoned inform user. Then suggest `--force` flag.
- [ ] Allow for path to subdirectory
- [ ] Figure out how to install TreeSitter per language
- [ ] Add Git hook
- [ ] Handle when there is new comment on already `extract`ed file
- [ ] Create `join-extract` command
- [ ] Write path to file as relative to repo

## Future plans

## Sumarry of 100 commits challange

It is really hard to be consistent in anything. But being consistent is one thing; keeping a project going through various changes is another.
Having strict rules that require you to add something to your project might be beneficial. It keeps you thinking about new changes and helps you remember what is already there. However, it also has downsides. For me, it was challenging to complete larger tasks.
In the end, I am happy that I tried to finish this challenge and create the tool that had been in the back of my mind for a long time. I applied changes as needed.

