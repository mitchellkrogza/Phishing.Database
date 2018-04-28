# domains2idna

## A tool to convert a domain or a file with a list of domain to the famous IDNA format.


* * *

# Tests

```shell
# The following run the tests.
$ python setup.py test
```

# Installation

You can install domain2idna with two ways.

```shell
# This install domain2idna without having to manually clone the repository
$ pip install -e git+https://github.com/funilrys/domain2idna.git#egg=domain2idna
```

```shell
# This install all dependencies along with domain2idna after you cloned the repository
$ pip install -e .
```

# Usage

## Import

```python
#!/usr/bin/env python3

"""
This module uses domains2idna to convert a given domain.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Contributors:
    Let's contribute to this example!!

Repository:
    https://github.com/funilrys/domain2idna
"""

from colorama import Style
from colorama import init as initiate

from domain2idna.core import Core

DOMAINS = [
    "bittréẋ.com", "bịllogram.com", "coinbȧse.com", "cryptopiạ.com", "cṙyptopia.com"
]

# We activate the automatical reset of string formatting
initiate(True)

# The following return the result of the whole loop.
print(
    "%sList of converted domains:%s %s"
    % (Style.BRIGHT, Style.RESET_ALL, Core(DOMAINS).to_idna())
)

# The following return the result of only one element.
print(
    "%sString representing a converted domain:%s %s"
    % (Style.BRIGHT, Style.RESET_ALL, Core(DOMAINS[-1]).to_idna())
)
```

## Command-Line

    usage: domain2idna [-h] [-d DOMAIN] [-f FILE] [-o OUTPUT]

    domain2idna - A tool to convert a domain or a file with a list of domain to
    the famous IDNA format.

    optional arguments:
    -h, --help            show this help message and exit
    -d DOMAIN, --domain DOMAIN
                        Set the domain to convert.
    -f FILE, --file FILE  Set the domain to convert.
    -o OUTPUT, --output OUTPUT
                        Set the file where we write the converted domain(s).

    Crafted with ♥ by Nissar Chababy (Funilrys)
