import json


input_no_comments = "main_no_comments.py"
input_comments_file_path = "just_comments.json"
output_comments_file_path = "with_comments_main.py"


def join_them(source_code, comments):
    for start_end, value in comments.items():  # Reverse to avoid offset issues
        start, _, end = start_end.partition(",")
        start, end = int(start), int(end)
        source_code = source_code[:start] + value + source_code[end:]

    return source_code


with open(input_no_comments, "r", encoding="utf-8") as file:
    source_code = file.read()

with open(input_comments_file_path, "r", encoding="utf-8") as file:
    comments = json.load(file)

done = join_them(source_code, comments)

with open(output_comments_file_path, "w", encoding="utf-8") as file:
    file.write(done)
