import json
from pathlib import Path


def apply_comments_to_file(comments_data, lines):
    adjusted_lines = lines

    # NOTE: this is absolutely horribly unoptimized
    # NOTE: but this is just PoC
    for line_to_append in comments_data["deleted_lines"]:
        adjusted_lines.insert(line_to_append, "")

    for comment in comments_data["comments"]:
        tmp = comment["start"]
        line_number, column = tmp["row"], tmp["column"]
        comment_text = comment["text"]
        if len(adjusted_lines[line_number]) == 0:
            adjusted_lines[line_number] = (
                " " * (column - len(adjusted_lines[line_number])) + comment_text + "\n"
            )
        elif len(adjusted_lines[line_number][:-1]) <= column:
            adjusted_lines[line_number] = (
                adjusted_lines[line_number][:-1].rstrip() + "  " + comment_text + "\n"
            )
        else:
            # TODO: it means something changed too much
            ...

            # print(
            #     line_number,
            #     repr(adjusted_lines[line_number]),
            #     len(adjusted_lines[line_number]),
            #     column,
            # )
            # raise ValueError
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
