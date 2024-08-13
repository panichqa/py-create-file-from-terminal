import sys
import os
from datetime import datetime


def parse_args() -> tuple[list[str], str]:
    args = sys.argv[1:]
    dir_path = []
    file_name = None

    if "-d" in args:
        d_index = args.index("-d")
        dir_path = args[d_index + 1:]
        if "-f" in dir_path:
            dir_path = dir_path[:dir_path.index("-f")]

    if "-f" in args:
        f_index = args.index("-f")
        if f_index + 1 < len(args):
            file_name = args[f_index + 1]

    return dir_path, file_name


def create_directory(path_list: list[str]) -> str:
    directory_path = os.path.join(*path_list)
    os.makedirs(directory_path, exist_ok=True)
    return directory_path


def collect_user_input() -> list[str]:
    lines = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"\n{current_time}\n")

    line_count = 1
    while True:
        line = input("Enter content line (type 'stop' to finish): ")
        if line.lower() == "stop":
            break
        lines.append(f"{line_count} {line}\n")
        line_count += 1

    return lines


def create_file(file_path: str, content: list[str]) -> None:
    with open(file_path, "a") as file:
        file.writelines(content)


def main() -> None:
    dir_path, file_name = parse_args()

    if dir_path:
        directory_path = create_directory(dir_path)
        if file_name:
            file_path = os.path.join(directory_path, file_name)
            content = collect_user_input()
            create_file(file_path, content)
    elif file_name:
        content = collect_user_input()
        create_file(file_name, content)
    else:
        raise ValueError(
            "Invalid arguments."
            " Use -d to specify directory or -f to specify file name."
        )


if __name__ == "__main__":
    main()
