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

Use `bip`:

```bash
python3 bip.py --help
# to extract
python3 bip.py extract path_to_file
# to join
python3 bip.py join path_to_file
```

(as the side effect the json file will be created)

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
