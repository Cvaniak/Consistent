import json


def apply_comments_to_file(comments_data, lines):
    adjusted_lines = lines

    for comment in comments_data["comments"]:
        line_number, column = comment["start"]
        comment_text = comment["text"]
        if len(adjusted_lines[line_number][:-1]) <= column:
            adjusted_lines[line_number] = (
                adjusted_lines[line_number][:-1]
                + " " * (column - len(adjusted_lines[line_number]))
                + comment_text
                + "\n"
            )
        else:
            print(
                line_number,
                repr(adjusted_lines[line_number]),
                len(adjusted_lines[line_number]),
                column,
            )
            raise ValueError

    return adjusted_lines


json_comments = "just_comments.json"
source_file_path = "main_no_comments.py"
output_file_path = "main_with_comments.py"

with open(json_comments, "r", encoding="utf-8") as json_file:
    comments_data = json.load(json_file)

with open(source_file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

done = apply_comments_to_file(comments_data, lines)

with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.writelines(done)
