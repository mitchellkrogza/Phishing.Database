#!/usr/bin/env python3

"""
domain2idna - A tool to convert a domain or a file with a list
of domain to the famous IDNA format.

This submodule will test domain2idna.helpers

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

from unittest import TestCase
from unittest import main as launch_tests

from domain2idna.helpers import File, path


class TestFile(TestCase):
    """
    This class will test helpers.File.
    """

    def test_write_delete(self):
        """
        This method test helpers.File.write along with helpers.File.delete.
        """

        expected = "Hello, World! I'm domain2idna"
        File("hi").write(expected)

        with open("hi") as file:
            actual = file.read()

        self.assertEqual(expected, actual)

        expected = False
        File("hi").delete()
        actual = path.isfile("hi")

        self.assertEqual(expected, actual)

    def test_write_overwrite_delete(self):
        """
        This metthod test helpers.File.write along with helpers.File.delete.
        """

        expected = "Hello, World! I'm domain2idna"
        File("hi").write(expected)

        with open("hi") as file:
            actual = file.read()

        self.assertEqual(expected, actual)

        expected = "Hello, World! Python is great, you should consider learning it!"
        File("hi").write(expected, overwrite=True)

        with open("hi") as file:
            actual = file.read()

        self.assertEqual(expected, actual)

        expected = False
        File("hi").delete()
        actual = path.isfile("hi")

        self.assertEqual(expected, actual)

    def test_read_delete(self):
        """
        This method test helpers.File.read along with helpers.File.delete.
        """

        expected = "Hello, World! This has been written by Fun Ilrys."
        File("hi").write(expected)
        actual = File("hi").read()

        self.assertEqual(expected, actual)

        expected = False
        File("hi").delete()
        actual = path.isfile("hi")

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
