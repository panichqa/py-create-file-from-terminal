import sys
import os
from datetime import datetime


def parse_args() -> str:
    args = sys.argv[1:]
    if "-d" in args:
        d_index = args.index("-d")
        dir_path = args[d_index + 1:]
    else:
        dir_path = []

    if "-f" in args:
        f_index = args.index("-f")
        file_name = args[f_index + 1]
    else:
        file_name = None

    return dir_path, file_name


def create_directory(path_list: list[str]) -> str:
    directory_path = os.path.join(*path_list)
    os.makedirs(directory_path, exist_ok=True)
    print(f'Directory "{directory_path}" created or already exists.')
    return directory_path


def create_file(file_path: str) -> None:
    with open(file_path, "a") as file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"\n{current_time}\n")
        line_count = 1
        while True:
            line = input(f"Enter content line {line_count}: ")
            if line.lower() == "stop":
                break
            file.write(f"{line_count} {line}\n")
            line_count += 1
    print(f'Content written to file "{file_path}".')


def main() -> None:
    args = sys.argv[1:]
    if "-d" in args:
        d_index = args.index("-d")
        path_list = []
        for i in range(d_index + 1, len(args)):
            if args[i] == "-f":
                break
            path_list.append(args[i])

        directory_path = create_directory(path_list)

        if "-f" in args:
            f_index = args.index("-f")
            if f_index + 1 < len(args):
                file_name = args[f_index + 1]
                file_path = os.path.join(directory_path, file_name)
                create_file(file_path)
    elif "-f" in args:
        f_index = args.index("-f")
        if f_index + 1 < len(args):
            file_name = args[f_index + 1]
            create_file(file_name)
    else:
        raise ValueError(
            "Invalid arguments."
            " Use -d to specify directory or -f to specify file name."
        )


if __name__ == "__main__":
    main()
