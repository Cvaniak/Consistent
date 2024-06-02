# Consistent

This repository is my attempt in [100 commits competition](https://100commitow.pl/).

## Project

My initial plan is to create tool/system that will allow you to write comments and notes in your project.
The catchy part is to keep them in separate file but display in the one with code.

---

## Demo

I need to record the example of usage.

## How to install

Not installable yet.

## How to use

`bip` is made of two main subcommands:

- `bip extract <file name>` which removes comments from code and place them in separate `JSON` file.
- `bip join <file name>` which applies comments from `JSON` file (if exists) in corresponding places.

By default (not changeable yet) `JSON` files are named as `comments_<original name>.json`.
So you can add to `.gitignore` line like `comments_*.json`.

## Supported languages

This tool uses `TreeSitter`. For every language the `AST` (Abstract Syntax Tree) has different nodes.
For this reason every language needs to be covered separately.

- [x] Python

## Problems

- When you use `join` command you can apply comments more than once

## TODO

- [x] Make it pip installable
- [ ] Fix double join
- [ ] When extracting, compare with current `JSON`
- [ ] Show abandoned comments
- [ ] Show deleted comments
- [ ] When `join` and comment is abandoned inform user. Then suggest `--force` flag.
- [ ] Allow for path to subdirectory
- [ ] Figure out how to install TreeSitter per language

## Future plans
