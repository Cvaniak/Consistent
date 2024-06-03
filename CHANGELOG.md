# Changelog

## Thought

- The usage of `TreeSitter` in theory can help to identify correct place for comment.
  The problem is that it have different attributes for every supported programming language.
- Even if the `Python` scripts are just for `PoC` I want to write some tests that will allow me to catch edge cases.

For now all tests are done on `Python` files, as the `TreeSitter` might work differently for other formats.

## Newest update

## 03.06.2024

In progress with creating demo.

## 18.05.2024

While extracting comments we should add info if they are alone in line or next to code.

## 15.05.2024

There is bug that if there is many lines comment then in diff_tree only one is attached.

Also the code works on files only in this repo (because we use commits from current repo).
We also need to handle situtaion where there is no repo.

## 10.05.2024

I wont be able to rewrite any of this to Rust as I planed initialy.
Instead I will focus to deliver working flow in Python.

I need to restructure my scripts and prepare them for pip install.

## 04.05.2024

At first I was worry that the JSON needs to keep only comment and minimum data.
But with this limitation it might be really hard to have good data structure.

New idea for data structure is to keep whole "branch" of AST (Abstract Syntax Tree) next to comment.
In each file there always be only unique "branches" like `class -> function -> variable`. It can be nested
any number of times but at the end there will be comment. It already should tell us where the comment should be placed.

## 03.05.2024

To address the problem of possible double injecting comments and double extracting I think JSON needs to be "DB" with all comments.
We always needs to think that JSON contains all comments, and we can just apply them on code no matter if there is already this comment or not.
To do so it might be helpful to think about better format structure that would keep not a row in code but something semantic.
Also when join algorithm is running it first should gather all the comments, throw them to JSON, resolve duplicates and then apply the comments.

## 29.04.2024

I run `extract_comments.py` and `join_comments.py` one after another on different Python source files to find edge cases.
If the source file is not same after two scripts it means that there might be edge case.

So far I found edge case related two variables defined in global space, which are under the `module` parent.

## 26.04.2024

Another day without progress, I do not have idea how to solve problem of many edge cases.

## 25.04.2024

I wrote some extension that would work with PREFIX. However my conclusion is that it still does not solve most of the problems.
Also I am overthinking the problem of situation when user is turning off comments, writing something and turning them on again (in a loop).

For now I need to focus to finish base idea and write down all needed features.

## 24.04.2024

The double join problem made me think that we need to have any kind of control over the state.
We can try to determine it on the fly or we can save it somewhere.
In both cases the problem is that user might mix the already saved comments with new one etc.
It will always create problems like the comments that are partially loaded or modified.

To prevent that I think that we can make the comments with prefix like `# LOCAL: this is comment`.
This way you see if the comments are loaded or not. You never delete comments that are not meant for deletion.
You can have commands that resolve better and easier any problems. They also should be easier to parse.

## 23.04.2024

The double usage of `join_comments.py` will modify the file twice. It needs to be solved.

## 19.04.2024

The main idea is ready. The diff algorithm for sure needs tweaks and more tests but its something to fix later.
Now I need a working flow. For this I will create CLI tool with options to choose.
Along the way the implementation of algorithms will probably change as well as JSON format and things I haven't thought about yet.

## 12.04.2024

After refactor and first test case I will probably continue with this approach. Now it is time to create tests for other files.

## 08.04.2024

After many hours I decided to check how `linting` tools manage tests.
This won't only be helpful in `PoC` but especially in final solution, where the tests will be crucial.

I decided to check the test code for `black` and `isort`. It is almost terrifying

## 07.04.2024

After small refactor of `extract_comments.py` and `join_comments.py` also the `diff_tree.py` needs one.
The biggest problem with this files is how to handle the files, so it will be easy to test, use, and put in to the flow.

## 03.04.2024

I need to rethink some design solutions. Nothing important today.

## 31.03.2024

This is Easter commit. So I can only offer an :egg:.

## 29.03.2024

So I am not very happy with current algorithm, but with some adjustments it should work well enough for proof of concept.
After tweaks I would like to prepare demo of how it can work in action.

## 24.03.2024

To summarize small research - we use `LCS` algorithm to find the `LCS` and then we see what is missing or what is new in newer file.
I will probably try to use old file with comments in, and just omit the fact of absence in newer one.

## 23.03.2024

Some research on most popular option to show the diff.
So it terns out that it is mostly `Longest Common Subsequence` (LCS).
With that knowledge I want to test algorithms that will allow me to identify the same nodes between code versions.

## 22.03.2024

Learning more about how to diff two `AST`s.
I want solution that will allow me to support users that forget or intentionally did not load the comments to the code.
In this situation I need to take last commits and parse thru all commits to current one tracking the position of nodes.

If all research will fail, I will probably build a workflow that will inform user about unsolved comments.

## 21.03.2024

The flow is working, you can use `main.py` to remove comments and `join_them.py` to place them in correct place again.
Next I want to check if I can use `TreeSitter` to find how the code changed between comments.

## 18.03.2024

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
