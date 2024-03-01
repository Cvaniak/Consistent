# Consistent

This repository is my attempt in [100 commits competition](https://100commitow.pl/).

For know `README` will be my way to keep track on this project.

## Project

My initial plan is to create tool/system that will allow you to write comments and notes in your project.  
The catchy part is to keep them in separate file but display in the one with code.

## Initial plan

This is how most of our comments will look like:

```python
def main():
    print("Hello World!") # This is my comment
```

The problem is that sometimes we want to include some comments or notes that should not go to public repository.

Lets call them **Comments of shame** but basically I mean private notes and thoughts.

My initial plan is to keep them in separate file:

```python
def main():
    print("Hello World!")
```

And maybe something like:

```bash
<function: main> <1st: print> <on the right> # This is my comment
```

The syntax is just to demonstrate idea.

## Approach

Options are many. The most difficult will be to keep comments in right place when code is modified or refactored.  
Probably there might be some idling comments and notes.

My smart ideas are to:

- Use **TreeSitter** or basically keep comments attached to Code Tree Element
- Force **LSP** to display them as `errors` or something
-

Difficult parts are:

- Abandoned comments
- How to enter the note/comment edition
- How to keep track on refactored function (moved from one place to another)
