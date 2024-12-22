# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT
import argparse
import sys
from textwrap import dedent
from .__about__ import __version__
from ._markitdown import MarkItDown, DocumentConverterResult

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
    metavar="outfilename",
    help="if unspecified, defaults to stdout",
)
parser.add_argument("--llm-client", choices={"OpenAI"}, help="default None")
parser.add_argument("--llm-client-url", help="base URL for --llm-client")
parser.add_argument("--llm-model", help="required for --llm-client")


def main(args=None):
    args = parser.parse_args(args)
    if args.llm_client == "OpenAI":
        from openai import OpenAI
        llm_client = OpenAI(base_url=args.llm_client_url)
    else:
        llm_client = None
    markitdown = MarkItDown(llm_client=llm_client, llm_model=args.llm_model)

    if args.filename:
        result = markitdown.convert(args.filename)
    else:
        result = markitdown.convert_stream(sys.stdin.buffer)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            print(result.text_content, file=f)
    else:
        print(result.text_content)


if __name__ == "__main__":
    main()
