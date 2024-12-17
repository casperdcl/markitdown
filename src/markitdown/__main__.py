# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import argparse
import sys
from textwrap import dedent
from .__about__ import __version__
from ._markitdown import MarkItDown, DocumentConverterResult


def main():
    parser = argparse.ArgumentParser(
        description="Convert various file formats to markdown.",
        prog="markitdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent(
            """\
            examples:
              markitdown example.pdf
              markitdown -o example.md example.pdf
              cat example.pdf | markitdown > example.md"""
        ),
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="show the version number and exit",
    )
    parser.add_argument(
        "filename", nargs="?", help="if unspecified, defaults to stdin"
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="filename",
        help="if unspecified, defaults to stdout",
    )

    args = parser.parse_args()
    markitdown = MarkItDown()

    if args.filename is None:
        result = markitdown.convert_stream(sys.stdin.buffer)
    else:
        result = markitdown.convert(args.filename)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            print(result.text_content, file=f)
    else:
        print(result.text_content)


if __name__ == "__main__":
    main()
