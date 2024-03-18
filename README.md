# Consistent

This repository is my attempt in [100 commits competition](https://100commitow.pl/).

For know `README` will be my way to keep track on this project.

## Project

My initial plan is to create tool/system that will allow you to write comments and notes in your project.  
The catchy part is to keep them in separate file but display in the one with code.

## Newest update

In progress with modifying `join_them` and `main` so we remove empty lines after comments:

```python
def foo():
    # comment
    # comment
    ...
```

Will be:

```python
def foo():
    ...

```

Not:

```python
def foo():


    ...
```

## 17.03.2024

`join_them.py` fixed.

Time to design flow with happy path and create little demo.

## 15.03.2024

The `join_them.py` must be fixed.

## 14.03.2024

In progress research of different comments standards.  
For example [TODO comments](https://github.com/stsewd/tree-sitter-comment).
That basically means that we could create some special syntax for our comments,  
or wrap this tool around `TODO comments`.

## 13.03.2024

I found [diffsitter](https://github.com/afnanenayet/diffsitter) which may help me
to find corresponding nodes between commits.

Not yet decide if I will use it as a part of the system or learn how it works to implement part of that.

## 11.03.2024

Today only some small tests without new results.

## 09.03.2024

Day spend on reading Tree Sitter documentation.  
New idea is to build flow around git hook.  
So the flow would go:

```
      | Load comments |
              V
  | Write code and comments |
              V
        | Save file |
              V
   | Run comment remover |
              V
  | Comments saved in file |
  | with commit id attached |
```

Now this flow is happy path. We have file with comments load to the same file from which we removed them.  
Problem begins if someone would not load comments right after.  
Then we can try to get commit in which they were removed,
load the old tree, load current tree and find corresponding nodes.  
Then we can apply the old comments to new file.

As a addition we can create messages of CLI tool that inform about hanging comments or other problems.

## 08.03.2024

At this moment comments are stored by their position in bytes in file.  
The better approach I am trying to implement is to put them via their connection with node or line in code.  
In version when we can store them by corresponding node, we can them push them in similar way to tree.  
The way to which node to attach them will be to determine if they are on the left from code or above another node.

## 06.03.2024

In `poc` there are two programs: `main.py` that removes comments from file
and put them to json file and `join_them.py` that merges two files together again.

Now I need more research to decide how to handle the flow.

## 03.03.2024

So we have working `comment remover`. Just few lines of code and we can remove comments from file.
The final solution will be probably in `Rust` but `PoCs` I will do in `Python`.

## 02.03.2024

So after more research I think that it may work similar to formatter or linter.  
You could write comment as normal, and on save it could collect all new comments and extract them too new file.  
It would give advantage of not changing the flow of writing comments.  
So the thing is that after collecting them we need to display them to user but also allow user to edit them.  
We can then have toggle mechanism that would load comments to file and the extract them, but it would mess up git on every toggle.

The project needs to start, so probably first step will be to do some PoC with tools like TreeSitter check if we can use existing CI/CD tools.

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
