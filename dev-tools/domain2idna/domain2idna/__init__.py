#!/usr/bin/env python3

"""
domain2idna - A tool to convert a domain or a file with a list
of domain to the famous IDNA format.

This submodule is the main entry of the module/library.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Contributors:
    Let's contribute to domains2idna!!

Repository:
    https://github.com/funilrys/domain2idna

License:
    MIT License

    Copyright (c) 2018 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import argparse
from colorama import Fore, Style
from colorama import init as initiate

from .core import Core
from .helpers import File


def domain(domain_to_convert, output=None):
    """
    This function convert the given domain to IDNA format.

    Arguments:
        - domain_to_convert: str
            The domain to convert
        - output: str
            The output of the conversion. If not set, we output to stdout.
    """

    if domain_to_convert:
        converted = Core(domain_to_convert).to_idna()

        if output:
            File(output).write(converted, overwrite=True)
        else:
            print(converted)
    else:
        raise Exception("Please give us a domain.")


def file(file_to_convert, output=None):
    """
    This function read a file and convert each line of the file to IDNA.

    Arguments:
        - file_to_convert: str
            The file to convert
        - output: str
            The output of the conversion. If not set, we output to stdout.
    """

    if file_to_convert:
        converted = []

        try:
            to_convert = File(file_to_convert).read().split("\n")
        except (UnicodeEncodeError, UnicodeDecodeError):
            to_convert = File(file_to_convert).read("ISO-8859-1").split("\n")

        converted = Core(to_convert).to_idna()

        if output:
            File(output).write("\n".join(converted), overwrite=True)
        else:
            print("\n".join(converted))


def command():
    """
    This function is the main entry of the command line script.
    """

    if __name__ == "domain2idna":
        initiate(True)

        parser = argparse.ArgumentParser(
            description="domain2idna - A tool to convert a domain or a file with \
            a list of domain to the famous IDNA format.",
            epilog="Crafted with %s by %s"
            % (
                Fore.RED + "♥" + Fore.RESET,
                Style.BRIGHT
                + Fore.CYAN
                + "Nissar Chababy (Funilrys)"
                + Style.RESET_ALL,
            ),
        )

        parser.add_argument(
            "-d", "--domain", type=str, help="Set the domain to convert."
        )

        parser.add_argument("-f", "--file", type=str, help="Set the domain to convert.")

        parser.add_argument(
            "-o",
            "--output",
            type=str,
            help="Set the file where we write the converted domain(s).",
        )

        args = parser.parse_args()

        if args.domain:
            domain(args.domain, args.output)
        elif args.file:
            file(args.file, args.output)
