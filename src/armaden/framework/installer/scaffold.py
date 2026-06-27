import argparse
import sys
from pathlib import Path

from armaden.framework.installer.generator import Generator, GeneratorResult


def _fmt_list(items: list[Path]) -> str:
    if not items:
        return "  (none)"
    return "\n".join(f"  + {item}" for item in items)


def _print_result(result: GeneratorResult) -> None:
    print()
    print("Directories created:")
    print(_fmt_list(result.created_dirs))
    print()
    print("Files created:")
    print(_fmt_list(result.created_files))
    if result.skipped_files:
        print()
        print("Skipped (already exist; use --force to overwrite):")
        print(_fmt_list(result.skipped_files))
    if result.errors:
        print()
        print("Errors:")
        for error in result.errors:
            print(f"  ! {error}")
        print()
        sys.exit(1)
    print()
    print(
        "Your application is ready. Set APP_DIR and run:\n"
        "  poetry run armaden\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="armaden-scaffold",
        description="Scaffold a new Armaden application in the current directory.",
    )
    parser.add_argument(
        "--name",
        default="My Application",
        help="Application name (default: 'My Application')",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Target directory (default: current directory)",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.exists():
        print(f"Error: path does not exist: {root}", file=sys.stderr)
        return 1
    if not root.is_dir():
        print(f"Error: path is not a directory: {root}", file=sys.stderr)
        return 1

    generator = Generator(root=root, force=args.force)
    result = generator.generate(name=args.name)
    _print_result(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
