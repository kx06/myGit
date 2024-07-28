import argparse
import os
import sys
from .data import MyGitFuncs


def parse_args():
    parser = argparse.ArgumentParser(
        description="A simple Git-like version control system"
    )
    commands = parser.add_subparsers(dest="command")
    commands.required = True

    init_parser = commands.add_parser("init", help="Initialize a new repository")
    init_parser.set_defaults(func=init)

    hash_object_parser = commands.add_parser(
        "hash-object", help="Compute object ID and optionally create a blob from a file"
    )
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument("file", help="File to hash")

    cat_file_parser = commands.add_parser(
        "cat-file", help="Provide content of repository object"
    )
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument("object", help="The object to display")

    return parser.parse_args()


def init(repo_funcs, args):
    try:
        repo_funcs.init()
        print(
            f"Initialized an empty mygit repository in {os.path.join(os.getcwd(), repo_funcs.GIT_DIR)}"
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def hash_object(repo_funcs, args):
    # try:
    with open(args.file, "rb") as f:
        content = f.read()
        print(repo_funcs.hash_object(content))
    # except FileNotFoundError:
    #     print(f"Error: File '{args.file}' not found", file=sys.stderr)
    #     sys.exit(1)
    # except Exception as e:
    #     print(f"Error: {e}", file=sys.stderr)
    #     sys.exit(1)


def cat_file(repo_funcs, args):
    try:
        sys.stdout.flush()
        sys.stdout.buffer.write(repo_funcs.get_object(args.object, extected=None))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    repo_funcs = MyGitFuncs()
    args = parse_args()
    args.func(repo_funcs, args)


if __name__ == "__main__":
    main()
