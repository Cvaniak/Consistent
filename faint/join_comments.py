import json
from pathlib import Path


def apply_comments_to_file(comments_data, lines):
    # NOTE: it modify original lines. Would need deep copy but might not be necessary
    adjusted_lines = lines

    for line_to_append in comments_data["deleted_lines"]:
        adjusted_lines.insert(line_to_append, "")

    for comment in comments_data["comments"]:
        tmp = comment["start"]
        line_number, column = tmp["row"], tmp["column"]
        comment_text = comment["text"]
        is_inline = comment["is_inline"]

        # NOTE: line is empty
        if not is_inline:
            adjusted_lines[line_number] = " " * column + comment_text + "\n"

        # NOTE: apply on right side of the code. Removes trailing spaces and apply exactly 2 spaces.
        elif len(adjusted_lines[line_number][:-1]) <= column:
            adjusted_lines[line_number] = adjusted_lines[line_number][:-1].rstrip() + "  " + comment_text + "\n"

        else:
            raise ValueError("It should not happen.")

    return adjusted_lines


def main(source_file_path: Path, output_file_path: Path, json_comments: Path):
    with open(json_comments, "r", encoding="utf-8") as json_file:
        comments_data = json.load(json_file)

    with open(source_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    done = apply_comments_to_file(comments_data, lines)

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.writelines(done)


if __name__ == "__main__":
    source_file_path = Path("main_no_comments.py")
    output_file_path = Path("main_with_comments.py")
    json_comments = Path("just_comments.json")
    main(source_file_path, output_file_path, json_comments)
