# PyFunceble

> A tool to check domains or IP availability (ACTIVE, INACTIVE, INVALID). Also described as "[an] excellent script for checking ACTIVE and INACTIVE domain names"

[![license](https://img.shields.io/github/license/funilrys/PyFunceble.svg)](https://github.com/funilrys/PyFunceble/blob/master/LICENSE) [![GitHub release](https://img.shields.io/github/release/funilrys/PyFunceble.svg)](https://github.com/funilrys/PyFunceble/releases/latest)

[![GitHub issues open](https://img.shields.io/github/issues/funilrys/PyFunceble.svg)]() [![GitHub closed issues](https://img.shields.io/github/issues-closed/funilrys/PyFunceble.svg)](https://github.com/funilrys/)

[![Github file size](https://img.shields.io/github/size/funilrys/PyFunceble/PyFunceble.py.svg)](https://github.com/funilrys/Pyfunceble/blob/master/PyFunceble)

The main idea behind this repository is to rewrite [Funceble](https://github.com/funilrys/funceble) into a more clean and portable format.

In other word the main idea behind this repository is to create a script the availability of a given domain, a hosts file or a list of domains by returning `ACTIVE`, `INACTIVE` or `INVALID`.

## :book: Wiki as place to be :star2::star2::star2:

Want to know more about **PyFunceble**? All information to know are under the [wiki](https://github.com/funilrys/PyFunceble/wiki)! You can also contribute there if you think that it's uncomplete!

You can get a copy of the wiki with the following:

```shell
git clone https://github.com/funilrys/PyFunceble.wiki.git
```

## Main Features

- Check the status of a given domain
- Read an existing file and check every domain present into it.
- Generate `hosts` file according to domain status with a custom IP.

- Show results on screen

- Save results on file(s)

- ... and a lot more !

--------------------------------------------------------------------------------

# Supporting the project

[PyFunceble](https://github.com/funilrys/PyFunceble), [Dead-Hosts](https://github.com/dead-hosts), [Funceble](https://github.com/funilrys/funceble) and all other analog projects are powered by :coffee:!

This project helps you and or you like it? [![Buy me a cup of coffee](https://img.shields.io/badge/Buy%20-me%20a%20cup%20of%20%E2%98%95-blue.svg)](https://www.paypal.me/funilrys/) :wink:

--------------------------------------------------------------------------------

# Contributors

Thanks to those awesome people for your awesome and crazy idea and or contributions which make or make **[Funceble](https://github.com/funilrys/funceble)** and (or indirectly) **[PyFunceble](https://github.com/funilrys/PyFunceble)** better.

```
 _______ _                 _          _                              _
|__   __| |               | |        | |                            | |
   | |  | |__   __ _ _ __ | | _____  | |_ ___    _   _  ___  _   _  | |
   | |  | '_ \ / _` | '_ \| |/ / __| | __/ _ \  | | | |/ _ \| | | | | |
   | |  | | | | (_| | | | |   <\__ \ | || (_) | | |_| | (_) | |_| | |_|
   |_|  |_| |_|\__,_|_| |_|_|\_\___/  \__\___/   \__, |\___/ \__,_| (_)
                                                  __/ |                
                                                 |___/
```

- Mitchell Krog - [@mitchellkrogza](https://github.com/mitchellkrogza)
- WaLLy3K - [@WaLLy3K](https://github.com/WaLLy3K)
- xxcriticxx - [@xxcriticxx](https://github.com/xxcriticxx)

--------------------------------------------------------------------------------

# Special Thanks

I would like to thank those awesome organization and people for

- Their current work
- Their awesome repository
- Their support
- Their promotion
- Their testings reports
- Their breaking reports
- Their contributions

which helped and/or still help me build and or test **[Funceble](https://github.com/funilrys/funceble)** and or **[PyFunceble](https://github.com/funilrys/PyFunceble)**.

```
 _______ _                 _          _                              _
|__   __| |               | |        | |                            | |
   | |  | |__   __ _ _ __ | | _____  | |_ ___    _   _  ___  _   _  | |
   | |  | '_ \ / _` | '_ \| |/ / __| | __/ _ \  | | | |/ _ \| | | | | |
   | |  | | | | (_| | | | |   <\__ \ | || (_) | | |_| | (_) | |_| | |_|
   |_|  |_| |_|\__,_|_| |_|_|\_\___/  \__\___/   \__, |\___/ \__,_| (_)
                                                  __/ |                
                                                 |___/
```

- Adam Warner - [@PromoFaux](https://github.com/PromoFaux)
- Mitchell Krog - [@mitchellkrogza](https://github.com/mitchellkrogza)
- Pi-Hole - [@pi-hole](https://github.com/pi-hole/pi-hole)
- SMed79 - [@SMed79](https://github.com/SMed79)

--------------------------------------------------------------------------------

# `hosts` files

## What is a hosts file?

A hosts file, named `hosts` (with no file extension), is a plain-text file used by all operating systems to map hostnames to IP addresses.

In most operating systems, the `hosts` file is preferential to `DNS`. Therefore if a domain is resolved by the `hosts` file, the request never leaves your computer.

Having a smart `hosts` file goes a long way towards blocking malware, adware, ransomware, porn and other nuisance websites.

A hosts file like this causes any lookups to any of the listed domains to resolve back to your localhost so it prevents any outgoing connections to the listed domains.

## Recommendations

I'd personally recommend using [Steven's hosts](https://github.com/StevenBlack/hosts), [Ultimate.Hosts.Blacklist](https://github.com/mitchellkrogza/Ultimate.Hosts.Blacklist) and/or [Pi-Hole](https://github.com/pi-hole/pi-hole) which are in my opinion the best out there.


--------------------------------------------------------------------------------

# License

```
MIT License

Copyright (c) 2017-2018 Nissar Chababy

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
```
