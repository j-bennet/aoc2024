import shutil
import sys
from os import path


def main(day_number):
    day_number = int(day_number)
    dir_name = f"d{day_number:02d}"
    if path.exists(dir_name):
        print(f"Directory {dir_name} already exists")
        sys.exit(1)
    shutil.copytree("template", dir_name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: prep.py <DAY>")
        sys.exit(1)
    main(sys.argv[1])
