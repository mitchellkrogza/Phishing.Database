"""
domain2idna - Python module/library to convert a domain or a file with a list
of domain to the famous IDNA format.

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
from unittest import TestLoader

from setuptools import setup


def _test_suite():
    """
    This method will discover and run all the test
    """

    test_loader = TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")
    return test_suite


setup(
    name="domain2idna",
    version="1.0.0",
    description="Python module/library to convert a domain or a file with a list \
     of domain to the famous IDNA format.",
    long_description=open("README").read(),
    author="funilrys",
    author_email="contact@funilrys.com",
    license="MIT https://raw.githubusercontent.com/funilrys/domain2idna/master/LICENSE",
    url="https://github.com/funilrys/domain2idna",
    platforms=["any"],
    packages=["domain2idna"],
    keywords=["Python", "domain", "idna"],
    classifiers=[
        "Environment :: Console",
        "Topic :: Internet",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    test_suite="setup._test_suite",
    entry_points={"console_scripts": ["domain2idna=domain2idna:command"]},
)
