#!/usr/bin/env python

"""
domain2idna - A tool to convert a domain or a file with a list
of domain to the famous IDNA format.

This module is the core of the module/library. It contains the brain of the program.

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


class Core(object):  # pylint: disable=too-few-public-methods
    """
    Brain of the program
    """

    def __init__(self, domains):
        self.domains = domains
        self.to_ignore = [
            "0.0.0.0",
            "localhost",
            "127.0.0.1",
            "localdomain",
            "local",
            "broadcasthost",
            "allhosts",
            "allnodes",
            "allrouters",
            "localnet",
            "loopback",
            "mcastprefix",
        ]

    @classmethod
    def convert_it_to_idna(cls, string):
        """
        This method convert the given string to IDNA.

        Argument:
            - string: str
                The string to convert.
        """

        return string.encode("idna").decode("utf-8")

    def to_idna(self):
        """
        This method convert a domain from the given list.

        Returns: str or list
            - str:
                if a single domain is given.
            - list:
                If a list of domain is given.
            The domain in IDNA format.
        """

        if isinstance(self.domains, list):
            result = []

            for domain in self.domains:
                if not domain.startswith("#"):
                    splited_domain = domain.split()
                    local_result = []

                    for element in splited_domain:

                        if element not in self.to_ignore:
                            try:
                                local_result.append(self.convert_it_to_idna(element))
                            except UnicodeError:
                                local_result.append(element)
                        else:
                            local_result.append(element)

                    result.append(" ".join(local_result))
                else:
                    result.append(domain)

            return result

        else:
            try:
                return self.domains.encode("idna").decode("utf-8")

            except UnicodeError:
                return self.domains
