# PoC

## How to run

First clone language tree sitter:

```bash
git clone https://github.com/tree-sitter/tree-sitter-python
```

Create (or not) `venv` and then install `requirements.txt`:

```bash
pip3 install -r requirements.txt
```

run:

```bash
python3 extract_comments.py
# or
python3 join_comments.py
# or
python3 diff_trees.py
```

to run tests:

```bash
pytest tests
```
