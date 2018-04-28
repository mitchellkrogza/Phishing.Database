#!/usr/bin/env python3

"""
domain2idna - A tool to convert a domain or a file with a list
of domain to the famous IDNA format.

This submodule contains all helpers that are used by other submodules.

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

from os import path, remove


class File(object):
    """
    File treatment/manipulations.

    Argument:
        file: str
            A path to the file to manipulate.
    """

    def __init__(self, file, auto_encoding=False):
        self.file = file
        self.auto_encoding = auto_encoding

    def write(self, data_to_write, overwrite=False):
        """
        Write or append data into the given file path.

        Argument:
            - data_to_write: str
                The data to write.
        """

        if data_to_write and isinstance(data_to_write, str):
            if overwrite or not path.isfile(self.file):
                with open(self.file, "w", encoding="utf-8") as file:
                    file.write(data_to_write)
            else:
                with open(self.file, "a", encoding="utf-8") as file:
                    file.write(data_to_write)

    def read(self, encoding=None):
        """
        Read a given file path and return its content.

        Returns: str
            The content of the given file path.
        """

        if not encoding:
            encoding = "utf-8"

        with open(self.file, "r", encoding=encoding) as file:
            funilrys = file.read()

        return funilrys

    def delete(self):
        """
        Delete a given file path.
        """

        try:
            remove(self.file)
        except OSError:
            pass
