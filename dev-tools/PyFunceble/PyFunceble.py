#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The tool to check domains or IP availability.


██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

PyFunceble is the little sister of Funceble (https://github.com/funilrys/funceble)
which was archived on March 13th, 2018.
At the end of 2017, PyFunceble was described by one of its most active user as:
"[an] excellent script for checking ACTIVE and INACTIVE domain names."

Our main objective is to test domains and IP availability
by generating an accurate result based on results from WHOIS, NSLOOKUP and
HTTP status codes.
As result, PyFunceble returns 3 status: ACTIVE, INACTIVE and INVALID.
The denomination of those statuses can be changed under your personal
`config.yaml`.

At the time we write this, PyFunceble is running actively and daily under 50+
Travis CI repository or process to test the availability of domains which are
present into hosts files, AdBlock filter lists, list of IP, list of domains or
blocklists.

An up to date explanation of all status can be found at https://git.io/vxieo.
You can also find a simple representation of the logic behind PyFunceble at
https://git.io/vxifw.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks to:
    Adam Warner - @PromoFaux
    Mitchell Krog - @mitchellkrogza
    Pi-Hole - @pi-hole
    SMed79 - @SMed79

Contributors:
    Let's contribute to PyFunceble!!

    Mitchell Krog - @mitchellkrogza
    Odyseus - @Odyseus
    WaLLy3K - @WaLLy3K
    xxcriticxx - @xxcriticxx

    The complete list can be found at https://git.io/vND4m

Original project link:
    https://github.com/funilrys/PyFunceble

Original project wiki:
    https://github.com/funilrys/PyFunceble/wiki

License: MIT
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
"""

# pylint: disable=too-many-lines,invalid-name,bad-continuation
import argparse
import hashlib
import socket
from collections import OrderedDict
from inspect import getsourcefile
from itertools import repeat
from json import decoder, dump, loads
from os import chmod, environ, mkdir, path, remove, rename
from os import sep as directory_separator
from os import stat, walk
from re import compile as comp
from re import escape
from re import sub as substrings
from stat import S_IEXEC
from subprocess import PIPE, Popen
from time import strftime

import requests
from colorama import Back, Fore, Style
from colorama import init as initiate
from yaml import load as load_yaml


class PyFunceble(object):  # pragma: no cover
    """
    Main entry to PYFunceble. Brain of the program. Also known as "put everything
    together to make the system works".

    Arguments:
        - domain: str
            A domain or IP to test.
        - file_path: str
            A path to a file to read.
    """

    def __init__(self, domain=None, file_path=None):
        if __name__ == "__main__":

            CONFIGURATION["file_to_test"] = file_path

            if CONFIGURATION["travis"]:
                AutoSave().travis_permissions()

            self.bypass()
            ExecutionTime("start")

            if domain:
                CONFIGURATION["domain"] = domain.lower()
                self.domain()
            elif file_path:
                self.file()

            ExecutionTime("stop")
            Percentage().log()

            if domain:
                self.colored_logo()
        else:
            CONFIGURATION["simple"] = CONFIGURATION["quiet"] = CONFIGURATION[
                "no_files"
            ] = True
            if domain:
                CONFIGURATION["domain"] = domain.lower()

    @classmethod
    def test(cls):
        """
        This method avoid confusion between self.domain which is called into
        __main__ and test() which should be called out of PyFunceble's scope.

        Returns: str
            ACTIVE, INACTIVE or INVALID.

        Raise:
            - Exception: when this method is called under __name___
        """

        if __name__ == "__main__":
            raise Exception(
                "You should not use this method. Please prefer self.domain()"
            )

        else:
            return ExpirationDate().get()

    @classmethod
    def bypass(cls):
        """
        Exit the script if `[PyFunceble skip]` is matched into the latest
        commit message.
        """

        regex_bypass = r"\[PyFunceble\sskip\]"

        if CONFIGURATION["travis"] and Helpers.Regex(
            Helpers.Command("git log -1").execute(), regex_bypass, return_data=False
        ).match():

            AutoSave(True, is_bypass=True)

    @classmethod
    def print_header(cls):
        """
        Decide if we print or not the header.
        """

        if not CONFIGURATION["quiet"] and not CONFIGURATION["header_printed"]:
            print("\n")
            if CONFIGURATION["less"]:
                Prints(None, "Less").header()
            else:
                Prints(None, "Generic").header()

            CONFIGURATION["header_printed"] = True

    def domain(self, domain=None, last_domain=None):
        """
        Manage the case that we want to test only a domain.

        Argument:
            - domain: str
                The domain or IP to test.
            - last_domain: str
                The last domain of the file we are testing.
        """

        if domain:
            CONFIGURATION["domain"] = self._format_domain(domain)
        self.print_header()

        if __name__ == "__main__":
            if CONFIGURATION["simple"]:
                print(ExpirationDate().get())
            else:
                status = ExpirationDate().get()

            if not CONFIGURATION["simple"] and CONFIGURATION["file_to_test"]:
                if CONFIGURATION["inactive_database"]:
                    if status == "ACTIVE":
                        Database().remove()
                    else:
                        Database().add()

                AutoContinue().backup()

                if domain != last_domain:
                    AutoSave()
                else:
                    ExecutionTime("stop")
                    Percentage().log()
                    self.reset_counters()
                    AutoContinue().backup()

                    self.colored_logo()

                    AutoSave(True)

            CONFIGURATION["http_code"] = ""
            CONFIGURATION["referer"] = ""
        else:
            ExpirationDate().get()
            return

    @classmethod
    def reset_counters(cls):
        """
        Reset the counters when needed.
        """

        for string in ["up", "down", "invalid", "tested"]:
            CONFIGURATION["counter"]["number"].update({string: 0})
        return

    @classmethod
    def colored_logo(cls):
        """
        This method print the colored logo based on global results.
        """

        if not CONFIGURATION["quiet"]:
            if CONFIGURATION["counter"]["percentage"]["up"] >= 50:
                print(Fore.GREEN + PYFUNCEBLE_LOGO)
            else:
                print(Fore.RED + PYFUNCEBLE_LOGO)

    @classmethod
    def _format_domain(cls, extracted_domain):
        """
        Format the extracted domain before passing it to the system.

        Argument:
            extracted_domain: str
                The extracted domain from the file.

        Returns: str
            The domain to test.
        """

        if not extracted_domain.startswith("#"):

            if "#" in extracted_domain:
                extracted_domain = extracted_domain[:extracted_domain.find("#")].strip()

            tabs = "\t"
            space = " "

            tabs_position, space_position = (
                extracted_domain.find(tabs), extracted_domain.find(space)
            )

            if tabs_position > -1 and space_position > -1:
                if space_position < tabs_position:
                    separator = space
                else:
                    separator = tabs
            elif tabs_position > -1:
                separator = tabs
            elif space_position > -1:
                separator = space
            else:
                separator = ""

            if separator:
                splited_line = extracted_domain.split(separator)

                index = 1
                while index < len(splited_line):
                    if splited_line[index]:
                        break

                    index += 1

                return splited_line[index]

            return extracted_domain

        return ""

    @classmethod
    def _format_adblock_decoded(cls, to_format, result=None):
        """
        Format the exctracted adblock line before passing it to the system.

        Arguments:
            - to_format: str
                The extracted line from the file.
            - result: None or list
                The list of extracted domain.

        Returns: list
            The list of extracted domains.
        """

        if not result:
            result = []

        for data in Helpers.List(to_format).format():
            if data:
                if "#" in data:
                    return cls._format_adblock_decoded(data.split("#"), result)

                elif "," in data:
                    return cls._format_adblock_decoded(data.split(","), result)

                elif "~" in data:
                    return cls._format_adblock_decoded(data.split("~"), result)

                elif "!" in data:
                    return cls._format_adblock_decoded(data.split("!"), result)

                elif "|" in data:
                    return cls._format_adblock_decoded(data.split("|"), result)

                elif data and (
                    ExpirationDate.is_domain_valid(data)
                    or ExpirationDate.is_ip_valid(data)
                ):
                    result.append(data)

        return result

    def adblock_decode(self, list_to_test):
        """
        Convert the adblock format into a readable format which is understood
        by the system.

        Argument:
            - list_to_test: A list, the read content of the given file.

        Returns: list
            The list of domain to test.
        """

        result = []
        regex = r"^(?:.*\|\|)([^\/\$\^]{1,}).*$"
        regex_v2 = r"(.*\..*)(?:#{1,}.*)"

        for line in list_to_test:
            rematch = Helpers.Regex(
                line, regex, return_data=True, rematch=True, group=0
            ).match()

            rematch_v2 = Helpers.Regex(
                line, regex_v2, return_data=True, rematch=True, group=0
            ).match()

            if rematch:
                result.extend(rematch)

            if rematch_v2:
                result.extend(
                    Helpers.List(self._format_adblock_decoded(rematch_v2)).format()
                )

        return result

    @classmethod
    def _extract_domain_from_file(cls):
        """
        This method extract all non commented lines.

        Returns: lis
            Each line of the file == an element of the list.
        """

        result = []

        if path.isfile(CONFIGURATION["file_to_test"]):
            with open(CONFIGURATION["file_to_test"]) as file:
                for line in file:
                    if not line.startswith("#"):
                        result.append(line.rstrip("\n").strip())
        else:
            raise FileNotFoundError(CONFIGURATION["file_to_test"])

        return result

    def file(self):
        """
        Manage the case that need to test each domain of a given file path.
        Note: 1 domain per line.
        """

        list_to_test = self._extract_domain_from_file()

        AutoContinue().restore()

        if CONFIGURATION["adblock"]:
            list_to_test = self.adblock_decode(list_to_test)
        else:
            list_to_test = list(map(self._format_domain, list_to_test))

        PyFunceble.Clean(list_to_test)

        if CONFIGURATION["inactive_database"]:
            Database().to_test()

            if CONFIGURATION["file_to_test"] in CONFIGURATION[
                "inactive_db"
            ] and "to_test" in CONFIGURATION[
                "inactive_db"
            ][
                CONFIGURATION["file_to_test"]
            ] and CONFIGURATION[
                "inactive_db"
            ][
                CONFIGURATION["file_to_test"]
            ][
                "to_test"
            ]:
                list_to_test.extend(
                    CONFIGURATION["inactive_db"][CONFIGURATION["file_to_test"]][
                        "to_test"
                    ]
                )

        regex_delete = r"localhost$|localdomain$|local$|broadcasthost$|0\.0\.0\.0$|allhosts$|allnodes$|allrouters$|localnet$|loopback$|mcastprefix$"  # pylint: disable=line-too-long

        list_to_test = Helpers.List(
            Helpers.Regex(list_to_test, regex_delete).not_matching_list()
        ).format()

        if CONFIGURATION["filter"]:
            list_to_test = Helpers.List(
                Helpers.Regex(
                    list_to_test, CONFIGURATION["filter"], escape=True
                ).matching_list()
            ).format()

        list(
            map(
                self.domain,
                list_to_test[CONFIGURATION["counter"]["number"]["tested"]:],
                repeat(list_to_test[-1]),
            )
        )

    @classmethod
    def switch(cls, variable):  # pylint: disable=inconsistent-return-statements
        """
        Switch CONFIGURATION variables to their opposite.

        Argument:
            - variable: str
                The CONFIGURATION[variable_name] to switch.

        Returns: bool
            The opposite of the installed value of Settings.variable_name.

        Raise:
            - Exception: When the configuration is not valid. In other words,
                if the CONFIGURATION[variable_name] is not a bool.
        """

        current_state = dict.get(CONFIGURATION, variable)

        if isinstance(current_state, bool):
            if current_state:
                return False

            return True

        to_print = "Please use the updater or post an issue to %s"

        raise Exception(to_print % LINKS["repo"] + "/issues.")

    class Clean(object):
        """
        Directory cleaning logic.
        This class clean the output/ directory.

        Argument:
            - list_to_test: list
                The list of domains to test.
        """

        def __init__(self, list_to_test):
            if list_to_test:
                try:
                    number_of_tested = CONFIGURATION["counter"]["number"]["tested"]

                    if number_of_tested == 0 or list_to_test[
                        number_of_tested - 1
                    ] == list_to_test[
                        -1
                    ] or number_of_tested == len(
                        list_to_test
                    ):
                        PyFunceble.reset_counters()

                        self.all()
                except IndexError:
                    PyFunceble.reset_counters()

                    self.all()
            else:
                self.all()

        @classmethod
        def file_to_delete(cls):
            """
            Return the list of file to delete.
            """

            directory = CURRENT_DIRECTORY + OUTPUTS["parent_directory"]

            if not directory.endswith(directory_separator):
                directory += directory_separator

            result = []

            for root, _, files in walk(directory):
                for file in files:
                    if file not in [".gitignore", ".keep"]:
                        if root.endswith(directory_separator):
                            result.append(root + file)
                        else:
                            result.append(root + directory_separator + file)

            return result

        def all(self):
            """
            Delete all discovered files.
            """

            to_delete = self.file_to_delete()

            for file in to_delete:
                Helpers.File(file).delete()


class AutoContinue(object):
    """
    Autocontinue logic/subsystem.
    """

    def __init__(self):
        if CONFIGURATION["auto_continue"]:
            self.autocontinue_log_file = CURRENT_DIRECTORY + OUTPUTS[
                "parent_directory"
            ] + OUTPUTS[
                "logs"
            ][
                "filenames"
            ][
                "auto_continue"
            ]

            if path.isfile(self.autocontinue_log_file):
                self.backup_content = Helpers.Dict().from_json(
                    Helpers.File(self.autocontinue_log_file).read()
                )
            else:
                self.backup_content = {}
                Helpers.File(self.autocontinue_log_file).write(str(self.backup_content))

    def backup(self):
        """
        Backup the current execution state.
        """

        if CONFIGURATION["auto_continue"]:
            data_to_backup = {}
            configuration_counter = CONFIGURATION["counter"]["number"]

            data_to_backup[CONFIGURATION["file_to_test"]] = {
                "tested": configuration_counter["tested"],
                "up": configuration_counter["up"],
                "down": configuration_counter["down"],
                "invalid": configuration_counter["invalid"],
            }

            to_save = {}

            to_save.update(self.backup_content)
            to_save.update(data_to_backup)

            Helpers.Dict(to_save).to_json(self.autocontinue_log_file)

    def restore(self):
        """
        Restore data from the given path.
        """

        file_to_restore = CONFIGURATION["file_to_test"]

        if CONFIGURATION["auto_continue"] and self.backup_content:
            if file_to_restore in self.backup_content:
                to_initiate = ["up", "down", "invalid", "tested"]

                alternatives = {
                    "up": "number_of_up",
                    "down": "number_of_down",
                    "invalid": "number_of_invalid",
                    "tested": "number_of_tested",
                }

                for string in to_initiate:
                    try:
                        CONFIGURATION["counter"]["number"].update(
                            {string: self.backup_content[file_to_restore][string]}
                        )
                    except KeyError:
                        CONFIGURATION["counter"]["number"].update(
                            {
                                string: self.backup_content[file_to_restore][
                                    alternatives[string]
                                ]
                            }
                        )


class AutoSave(object):  # pragma: no cover  # pylint: disable=too-few-public-methods
    """
    Logic behind autosave.

    Arguments:
        - is_last_domain: bool
            Tell the autosave logic if we are at the end.
        - is_bypass: bool
            Tell the autosave logic if we are in bypass mode.
    """

    def __init__(self, is_last_domain=False, is_bypass=False):
        if CONFIGURATION["travis"]:
            self.last = is_last_domain
            self.bypass = is_bypass
            self._travis()

    @classmethod
    def travis_permissions(cls):
        """
        Set permissions in order to avoid issues before commiting.
        """
        try:
            build_dir = environ["TRAVIS_BUILD_DIR"]
            commands = [
                "sudo chown -R travis:travis %s" % (build_dir),
                "sudo chgrp -R travis %s" % (build_dir),
                "sudo chmod -R g+rwX %s" % (build_dir),
                "sudo chmod 777 -Rf %s.git" % (build_dir + directory_separator),
                r"sudo find %s -type d -exec chmod g+x '{}' \;" % (build_dir),
            ]

            for command in commands:
                Helpers.Command(command).execute()

            if Helpers.Command("git config core.sharedRepository").execute() == "":
                Helpers.Command("git config core.sharedRepository group").execute()
        except KeyError:
            pass

    def _travis(self):
        """
        Logic behind travis autosave.
        """

        current_time = int(strftime("%s"))
        time_autorisation = False

        try:
            time_autorisation = current_time >= int(CONFIGURATION["start"]) + (
                int(CONFIGURATION["travis_autosave_minutes"]) * 60
            )
        except KeyError:
            if self.last and not self.bypass:
                raise Exception("Please review the way `ExecutionTime()` is called.")

        if self.last or time_autorisation or self.bypass:
            Percentage().log()
            self.travis_permissions()

            command = 'git add --all && git commit -a -m "%s"'

            if self.last or self.bypass:
                if CONFIGURATION["command_before_end"]:
                    Helpers.Command(CONFIGURATION["command_before_end"]).execute()

                message = CONFIGURATION["travis_autosave_final_commit"] + " [ci skip]"

                Helpers.Command(command % message).execute()
            else:
                Helpers.Command(
                    command % CONFIGURATION["travis_autosave_commit"]
                ).execute()

            Helpers.Command(
                "git push origin %s" % CONFIGURATION["travis_branch"]
            ).execute()
            exit(0)


class Database(object):
    """
    Logic behind the generation and the usage of a database system.
    The main idea behind this is to provide an inactive-db.json and test all
    inactive domain which are into to it regularly
    """

    def __init__(self):
        self.file_path = CONFIGURATION["file_to_test"]
        self.current_time = int(strftime("%s"))
        self.day_in_seconds = CONFIGURATION["days_between_db_retest"] * 24 * 3600
        self.inactive_db_path = CURRENT_DIRECTORY + OUTPUTS["default_files"][
            "inactive_db"
        ]

    def _retrieve(self):
        """
        Return the current content of the inactive-db.json file.
        """

        if path.isfile(self.inactive_db_path):
            CONFIGURATION["inactive_db"] = Helpers.Dict().from_json(
                Helpers.File(self.inactive_db_path).read()
            )
        else:
            CONFIGURATION["inactive_db"] = {}

        return

    def _backup(self):
        """
        Save the current database into the inactive-db.json file.
        """

        if CONFIGURATION["inactive_database"]:
            Helpers.Dict(CONFIGURATION["inactive_db"]).to_json(self.inactive_db_path)

    def _add_to_test(self, to_add):
        """
        Add an element or a list of element into
        CONFIGURATION['inactive_db'][self.file_path]['to_test'].

        Argument:
            - to_add: str
                The domain or ip to add.
        """

        if not isinstance(to_add, list):
            to_add = [to_add]

        if self.file_path in CONFIGURATION["inactive_db"]:
            if "to_test" in CONFIGURATION["inactive_db"][self.file_path]:
                CONFIGURATION["inactive_db"][self.file_path]["to_test"].extend(to_add)
            else:
                CONFIGURATION["inactive_db"][self.file_path]["to_test"] = to_add
        else:
            CONFIGURATION["inactive_db"].update({self.file_path: {"to_test": to_add}})

        self._backup()

    def to_test(self):
        """
        Get the list to test for the next session.
        """

        result = []
        to_delete = []

        self._retrieve()

        if self.file_path in CONFIGURATION["inactive_db"]:
            for data in CONFIGURATION["inactive_db"][self.file_path]:
                if data != "to_test":
                    if self.current_time > int(data) + self.day_in_seconds:
                        result.extend(
                            CONFIGURATION["inactive_db"][self.file_path][data]
                        )
                        to_delete.append(data)

            Helpers.Dict(CONFIGURATION["inactive_db"][self.file_path]).remove_key(
                to_delete
            )

            self._add_to_test(result)
        else:
            CONFIGURATION["inactive_db"].update({self.file_path: {}})

        self._backup()

    def _timestamp(self):
        """
        Return the timestamp where we are going to save our current list.

        Returns: int or str
            The timestamp to append with the currently tested domains.
        """

        result = 0
        to_delete = []

        if self.file_path in CONFIGURATION["inactive_db"] and CONFIGURATION[
            "inactive_db"
        ][
            self.file_path
        ]:
            for data in CONFIGURATION["inactive_db"][self.file_path]:
                if data != "to_test":
                    if self.current_time < int(data) + self.day_in_seconds:
                        result = int(data)
                    else:
                        result = self.current_time
                        to_delete.append(data)

            for element in to_delete:
                self._add_to_test(CONFIGURATION["inactive_db"][self.file_path][element])
            Helpers.Dict(CONFIGURATION["inactive_db"][self.file_path]).remove_key(
                to_delete
            )

            return result

        return self.current_time

    def add(self):
        """
        Save the current CONFIGURATION['domain'] into the current timestamp.
        """

        timestamp = str(self._timestamp())

        if self.file_path in CONFIGURATION["inactive_db"]:
            if timestamp in CONFIGURATION["inactive_db"][self.file_path]:
                if CONFIGURATION["domain"] not in CONFIGURATION["inactive_db"][
                    self.file_path
                ][
                    timestamp
                ]:
                    CONFIGURATION["inactive_db"][self.file_path][timestamp].append(
                        CONFIGURATION["domain"]
                    )
            else:
                CONFIGURATION["inactive_db"][self.file_path].update(
                    {timestamp: [CONFIGURATION["domain"]]}
                )

            if "to_test" in CONFIGURATION["inactive_db"][
                self.file_path
            ] and CONFIGURATION[
                "domain"
            ] in CONFIGURATION[
                "inactive_db"
            ][
                self.file_path
            ][
                "to_test"
            ]:
                CONFIGURATION["inactive_db"][self.file_path]["to_test"].remove(
                    CONFIGURATION["domain"]
                )
        else:
            CONFIGURATION["inactive_db"][self.file_path] = {
                timestamp: [CONFIGURATION["domain"]]
            }

        self._backup()

    def remove(self):
        """
        Remove all occurence of CONFIGURATION['domain'] into the database.
        """

        if self.file_path in CONFIGURATION["inactive_db"]:
            for data in CONFIGURATION["inactive_db"][self.file_path]:
                if CONFIGURATION["domain"] in CONFIGURATION["inactive_db"][
                    self.file_path
                ][
                    data
                ]:
                    CONFIGURATION["inactive_db"][self.file_path][data].remove(
                        CONFIGURATION["domain"]
                    )

        self._backup()


class ExecutionTime(object):  # pylint: disable=too-few-public-methods
    """
    Set and return the exection time of the program.

    Arguments:
        - action: 'start' or 'stop'
        - return_result: bool
            True: we return the execution time.
            False: we return nothing.
    """

    def __init__(self, action="start"):
        if CONFIGURATION["show_execution_time"] or CONFIGURATION["travis"]:
            if action == "start":
                self._starting_time()
            elif action == "stop":
                self._stoping_time()

                print(
                    Fore.MAGENTA
                    + Style.BRIGHT
                    + "\nExecution Time: "
                    + self.format_execution_time()
                )

    @classmethod
    def _starting_time(cls):
        """
        Set the starting time.
        """

        CONFIGURATION["start"] = int(strftime("%s"))

    @classmethod
    def _stoping_time(cls):
        """
        Set the ending time.
        """

        CONFIGURATION["end"] = int(strftime("%s"))

    @classmethod
    def _calculate(cls):
        """
        calculate the difference between starting and ending time.

        Returns: dict
            A dics with `days`,`hours`,`minutes` and `seconds`.
        """

        time_difference = CONFIGURATION["end"] - CONFIGURATION["start"]

        data = OrderedDict()

        data["days"] = str((time_difference // 24) % 24).zfill(2)
        data["hours"] = str(time_difference // 3600).zfill(2)
        data["minutes"] = str((time_difference % 3600) // 60).zfill(2)
        data["seconds"] = str(time_difference % 60).zfill(2)

        return data

    def format_execution_time(self):
        """
        Format the calculated time into a human readable format.

        Returns: str
            A human readable date.
        """

        result = ""
        calculated_time = self._calculate()
        times = list(calculated_time.keys())

        for time in times:
            result += calculated_time[time]

            if time != times[-1]:
                result += ":"

        return result


class Prints(object):
    """
    Print data on screen and into a file if needed.
    Template Possibilities: Percentage, Less, HTTP and any status you want.

    Arguments:
        - to_print: list
            The list of data to print.
        - template: str
            The template to use.
        - output_file: str
            The path to the file to write.
        - only_on_file: bool
            True: We don't print data on screen.
            False: We print data on screen.
    """

    def __init__(self, to_print, template, output_file=None, only_on_file=False):
        self.template = template
        self.output = output_file
        self.data_to_print = to_print
        self.only_on_file = only_on_file

        self.headers = OrderedDict()

        self.headers["Generic"] = OrderedDict(
            zip(
                [
                    "Domain",
                    "Status",
                    "Expiration Date",
                    "Source",
                    "HTTP Code",
                    "Analyze Date",
                ],
                [100, 11, 17, 10, 10, 20],
            )
        )

        self.headers[STATUS["official"]["up"]] = OrderedDict(
            zip(
                ["Domain", "Expiration Date", "Source", "HTTP Code", "Analyze Date"],
                [100, 17, 10, 10, 20],
            )
        )

        self.headers[STATUS["official"]["down"]] = OrderedDict(
            zip(
                [
                    "Domain",
                    "WHOIS Server",
                    "Status",
                    "Source",
                    "HTTP Code",
                    "Analyze Date",
                ],
                [100, 35, 11, 10, 10, 20],
            )
        )

        self.headers[STATUS["official"]["invalid"]] = OrderedDict(
            zip(["Domain", "Source", "HTTP Code", "Analyze Date"], [100, 10, 10, 20])
        )

        self.headers["Less"] = OrderedDict(
            zip(["Domain", "Status", "HTTP Code"], [100, 11, 10])
        )

        self.headers["Percentage"] = OrderedDict(
            zip(["Status", "Percentage", "Numbers"], [11, 12, 12])
        )

        self.headers["HTTP"] = OrderedDict(
            zip(["Domain", "Status", "HTTP Code", "Analyze Date"], [100, 11, 10, 20])
        )

        self.currently_used_header = {}

    def before_header(self):
        """
        Print informations about PyFunceble and the date of generation of a file
        into a given path, if doesn't exist.
        """

        if not CONFIGURATION["no_files"] and self.output and not path.isfile(
            self.output
        ):
            link = ("# File generated with %s\n" % LINKS["repo"])
            date_of_generation = ("# Date of generation: %s \n\n" % CURRENT_TIME)

            Helpers().File(self.output).write(link + date_of_generation)

    @classmethod
    def _header_constructor(cls, data_to_print, separator="-"):
        """
        Construct header of the table according to template.

        Arguments:
            - data_to_print: list
                The list of data to print into the header.
            - separator: str
                The separator to use for the table header generation.

        Returns: list
            The data to print in list format.
        """

        header_data = []
        header_size = ""
        before_size = "%-"
        after_size = "s "

        if separator:
            separator_data = []

        for data in data_to_print:
            size = data_to_print[data]
            header_data.append(data)

            header_size += before_size + str(size) + after_size

            if separator:
                separator_data.append(separator * size)

        if separator:
            return [
                header_size % tuple(header_data), header_size % tuple(separator_data)
            ]

        return [header_size % tuple(header_data)]

    def header(self, do_not_print=False):  # pylint: disable=too-many-branches
        """
        Management and creation of templates of header.
        Please consider as "header" the title of each columns.
        """

        if not CONFIGURATION[
            "header_printed"
        ] or self.template == "Percentage" or do_not_print:
            if self.template.lower() in STATUS["list"][
                "generic"
            ] or self.template == "Generic_File":
                to_print = self.headers["Generic"]

                if self.template.lower() in STATUS["list"]["generic"]:
                    to_print = Helpers.Dict(to_print).remove_key("Analyze Date")
            if self.template.lower() in STATUS["list"]["up"]:
                to_print = self.headers[STATUS["official"]["up"]]
            elif self.template.lower() in STATUS["list"]["down"]:
                to_print = self.headers[STATUS["official"]["down"]]
            elif self.template.lower() in STATUS["list"]["invalid"]:
                to_print = self.headers[STATUS["official"]["invalid"]]
            elif self.template == "Less" or self.template == "Percentage" or self.template == "HTTP":  # pylint: disable=line-too-long
                to_print = self.headers[self.template]

                if self.template == "Less" and not HTTP_CODE["active"]:
                    to_print["Source"] = 10

            if not HTTP_CODE["active"]:
                to_print = Helpers.Dict(to_print).remove_key("HTTP Code")

            self.currently_used_header = to_print

            if not do_not_print:
                self.before_header()
                for formated_template in self._header_constructor(to_print):
                    if not self.only_on_file:
                        print(formated_template)
                    if self.output:
                        Helpers.File(self.output).write(formated_template + "\n")

    def _data_constructor(self, size):
        """
        Construct the table of data according to given size.

        Argument:
            - size: list
                The maximal length of each string in the table.

        Returns: OrderedDict
            An dict with all information about the data and how to which what
            maximal size to print it.

        Raise:
            - Exception: if the data and the size does not have the same length.
        """

        result = OrderedDict()
        if len(self.data_to_print) == len(size):
            for i in range(len(self.data_to_print)):
                result[self.data_to_print[i]] = size[i]
        else:
            # This should never happend. If it's happens then there is something
            # wrong from the inputed data.
            raise Exception(
                "Inputed: " + str(len(self.data_to_print)) + "; Size: " + str(len(size))
            )

        return result

    @classmethod
    def _size_from_header(cls, header):
        """
        Get the size of each columns from the header.

        Argument:
            - header_type: dict
                The header we have to get the size from.

        Returns: list
            The maximal size of the each data to print.
        """

        result = []

        for data in header:
            result.append(header[data])

        return result

    def _colorify(self, data):
        """
        Retun colored string.

        Argument:
            - data: str
                The string to colorify.

        Returns: str
            A colored string.
        """

        if self.template in ["Generic", "Less"]:
            if self.data_to_print[1].lower() in STATUS["list"]["up"]:
                data = Fore.BLACK + Back.GREEN + data
            elif self.data_to_print[1].lower() in STATUS["list"]["down"]:
                data = Fore.BLACK + Back.RED + data
            else:
                data = Fore.BLACK + Back.CYAN + data
        return data

    def data(self):
        """
        Management and input of data to the table.

        Raise:
            - Exception: When self.data_to_print is not a list.
        """

        if isinstance(self.data_to_print, list):
            to_print = {}
            to_print_size = []

            alone_cases = ["Percentage", "HTTP"]
            without_header = ["FullHosts", "PlainDomain"]

            if self.template not in alone_cases and self.template not in without_header:
                self.header(True)
                to_print_size = self._size_from_header(self.currently_used_header)
            elif self.template in without_header:
                for data in self.data_to_print:
                    to_print_size.append(str(len(data)))
            else:
                to_print_size = self._size_from_header(self.headers[self.template])

            to_print = self._data_constructor(to_print_size)

            self.before_header()

            for data in self._header_constructor(to_print, False):
                if self.template.lower() in STATUS["list"][
                    "generic"
                ] or self.template in [
                    "Less", "Percentage"
                ]:
                    if not self.only_on_file:
                        data = self._colorify(data)
                        print(data)
                if not CONFIGURATION["no_files"] and self.output:
                    Helpers.File(self.output).write(data + "\n")
        else:
            # This should never happend. If it's happens then there's a big issue
            # around data_to_print.
            raise Exception("Please review Prints().data()")


class HTTPCode(object):  # pylint: disable=too-few-public-methods
    """
    Get and return the HTTP code status of a given domain.
    """

    @classmethod
    def _access(cls):
        """
        Get the HTTP code status.

        Returns: int or None
            int: The catched HTTP status_code.
            None: Nothing catched.
        """

        try:
            try:
                try:
                    req = requests.head(
                        "http://%s:80" % CONFIGURATION["domain"],
                        timeout=CONFIGURATION["seconds_before_http_timeout"],
                    )
                except socket.timeout:
                    return None

            except requests.exceptions.Timeout:
                return None

            return req.status_code

        except requests.ConnectionError:
            return None

    def get(self):
        """
        Return the HTTP code status.

        Returns: str or int
            str: if no status_code is catched.
            int: the status_code.
        """

        http_code = self._access()
        list_of_valid_http_code = []

        for codes in [
            HTTP_CODE["list"]["up"],
            HTTP_CODE["list"]["potentially_down"],
            HTTP_CODE["list"]["potentially_up"],
        ]:
            list_of_valid_http_code.extend(codes)

        if http_code not in list_of_valid_http_code or http_code is None:
            return "*" * 3

        return http_code


class Lookup(object):
    """
    This class can be used to NSLOOKUP or WHOIS lookup.
    """

    @classmethod
    def nslookup(cls):
        """
        Implementation of UNIX nslookup.
        """

        try:
            try:
                try:
                    socket.getaddrinfo(
                        CONFIGURATION["domain"], 80, 0, 0, socket.IPPROTO_TCP
                    )
                except OSError:
                    return False

            except socket.herror:
                return False

            return True

        except socket.gaierror:
            return False

    @classmethod
    def whois(cls, whois_server, domain=None, timeout=None):
        """
        Implementation of UNIX whois.

        Arguments:
            - whois_server: str
                The whois server to use to get the record.
            - domain: str
                The domain to get the whois record from.
            - timeout: int
                The timeout to apply to the request.

        Returns: None or str
            None: No whois record catched.
            str: The whois record.
        """

        if domain is None:
            domain = CONFIGURATION["domain"]

        if timeout is None:
            timeout = CONFIGURATION["seconds_before_http_timeout"]

        if whois_server:

            req = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if CONFIGURATION["seconds_before_http_timeout"] % 3 == 0:
                req.settimeout(timeout)
            else:
                req.settimeout(3)

            try:
                req.connect((whois_server, 43))
            except socket.error:
                return None

            req.send((domain + "\r\n").encode())
            response = b""

            while True:
                try:
                    try:
                        data = req.recv(4096)
                    except ConnectionResetError:
                        req.close()

                        return None

                except socket.timeout:
                    req.close()

                    return None

                response += data
                if not data:
                    break

            req.close()

            try:
                return response.decode()

            except UnicodeDecodeError:
                return response.decode("utf-8", "replace")

        return None


class Percentage(object):
    """
    Calculation of the percentage of each status.

    Arguments:
        - domain_status: str
            The status to increment.
        - init: None or dict
            None: we start from 0.
            dict: we start from the passed data.
    """

    def __init__(self, domain_status=None, init=None):
        self.status = domain_status

        if init and isinstance(init, dict):
            for data in init:
                CONFIGURATION["counter"]["percentage"].update({data: init[data]})

    def count(self):
        """
        Count the number of domain for each status.
        """

        if self.status:
            CONFIGURATION["counter"]["number"]["tested"] += 1

            if self.status.lower() in STATUS["list"]["up"]:
                CONFIGURATION["counter"]["number"]["up"] += 1
            elif self.status.lower() in STATUS["list"]["down"]:
                CONFIGURATION["counter"]["number"]["down"] += 1
            else:
                CONFIGURATION["counter"]["number"]["invalid"] += 1

    @classmethod
    def _calculate(cls):
        """
        Calculate the percentage of each status.
        """

        percentages = {
            "up": CONFIGURATION["counter"]["number"]["up"],
            "down": CONFIGURATION["counter"]["number"]["down"],
            "invalid": CONFIGURATION["counter"]["number"]["invalid"],
        }

        for percentage in percentages:
            calculation = percentages[percentage] * 100 // CONFIGURATION["counter"][
                "number"
            ][
                "tested"
            ]
            CONFIGURATION["counter"]["percentage"].update({percentage: calculation})

    def log(self):
        """
        Print on screen and on file the percentages for each status.
        """

        if CONFIGURATION["show_percentage"] and CONFIGURATION["counter"]["number"][
            "tested"
        ] > 0:
            output = CURRENT_DIRECTORY + OUTPUTS["parent_directory"] + OUTPUTS["logs"][
                "directories"
            ][
                "parent"
            ] + OUTPUTS[
                "logs"
            ][
                "directories"
            ][
                "percentage"
            ] + OUTPUTS[
                "logs"
            ][
                "filenames"
            ][
                "percentage"
            ]
            Helpers.File(output).delete()

            self._calculate()

            if not CONFIGURATION["quiet"]:
                print("\n")
                Prints(None, "Percentage", output).header()

                for to_print in [
                    [
                        STATUS["official"]["up"],
                        str(CONFIGURATION["counter"]["percentage"]["up"]) + "%",
                        CONFIGURATION["counter"]["number"]["up"],
                    ],
                    [
                        STATUS["official"]["down"],
                        str(CONFIGURATION["counter"]["percentage"]["down"]) + "%",
                        CONFIGURATION["counter"]["number"]["down"],
                    ],
                    [
                        STATUS["official"]["invalid"],
                        str(CONFIGURATION["counter"]["percentage"]["invalid"]) + "%",
                        CONFIGURATION["counter"]["number"]["invalid"],
                    ],
                ]:
                    Prints(to_print, "Percentage", output).data()


class Generate(object):
    """
    Generate different sort of files.

    Arguments:
        - domain_status: str
            The domain status.
        - source: str
            The source of the given status.
        - expiration_date: str
            The expiration date of the domain if catched.
    """

    def __init__(self, domain_status, source=None, expiration_date=None):
        self.domain_status = domain_status
        self.source = source
        self.expiration_date = expiration_date

        self.output_parent_dir = CURRENT_DIRECTORY + OUTPUTS["parent_directory"]

        self.refer_status = ""
        self.output = ""

    def hosts_file(self):
        """
        Generate a hosts file.
        """

        if CONFIGURATION["generate_hosts"] or CONFIGURATION["plain_list_domain"]:
            splited_destination = ""

            output_hosts = self.output_parent_dir + OUTPUTS["hosts"][
                "directory"
            ] + "%s" + directory_separator + OUTPUTS[
                "hosts"
            ][
                "filename"
            ]

            output_domains = self.output_parent_dir + OUTPUTS["domains"][
                "directory"
            ] + "%s" + directory_separator + OUTPUTS[
                "domains"
            ][
                "filename"
            ]

            if self.domain_status.lower() in STATUS["list"]["up"]:
                hosts_destination = output_hosts % STATUS["official"]["up"]
                plain_destination = output_domains % STATUS["official"]["up"]
            elif self.domain_status.lower() in STATUS["list"]["down"]:
                hosts_destination = output_hosts % STATUS["official"]["down"]
                plain_destination = output_domains % STATUS["official"]["down"]
            elif self.domain_status.lower() in STATUS["list"]["invalid"]:
                hosts_destination = output_hosts % STATUS["official"]["invalid"]
                plain_destination = output_domains % STATUS["official"]["invalid"]
            elif self.domain_status.lower() in STATUS["list"][
                "potentially_up"
            ] or self.domain_status.lower() in STATUS[
                "list"
            ][
                "potentially_down"
            ] or self.domain_status.lower() in STATUS[
                "list"
            ][
                "http_active"
            ]:

                output_dir = self.output_parent_dir + OUTPUTS["http_analytic"][
                    "directories"
                ][
                    "parent"
                ]
                if self.domain_status.lower() in STATUS["list"]["potentially_up"]:
                    output_dir += OUTPUTS["http_analytic"]["directories"][
                        "potentially_up"
                    ]
                elif self.domain_status.lower() in STATUS["list"]["potentially_down"]:
                    output_dir += OUTPUTS["http_analytic"]["directories"][
                        "potentially_down"
                    ]
                else:
                    output_dir += OUTPUTS["http_analytic"]["directories"]["up"]

                if not output_dir.endswith(directory_separator):
                    output_dir += directory_separator

                hosts_destination = output_dir + OUTPUTS["hosts"]["filename"]
                plain_destination = output_dir + OUTPUTS["domains"]["filename"]
                splited_destination = output_dir + str(CONFIGURATION["http_code"])

            if CONFIGURATION["generate_hosts"]:
                Prints(
                    [CONFIGURATION["custom_ip"], CONFIGURATION["domain"]],
                    "FullHosts",
                    hosts_destination,
                ).data()

            if CONFIGURATION["plain_list_domain"]:
                Prints(
                    [CONFIGURATION["domain"]], "PlainDomain", plain_destination
                ).data()

            if CONFIGURATION["split"] and splited_destination:
                Prints(
                    [CONFIGURATION["domain"]], "PlainDomain", splited_destination
                ).data()

    def unified_file(self):
        """
        Generate unified file. Understand by that that we use an unified table
        instead of a separate table for each status which could result into a
        misunderstanding.
        """

        if CONFIGURATION["unified"]:
            output = self.output_parent_dir + OUTPUTS["default_files"]["results"]
            if CONFIGURATION["less"]:
                if HTTP_CODE["active"]:
                    to_print = [
                        CONFIGURATION["domain"],
                        self.domain_status,
                        CONFIGURATION["http_code"],
                    ]
                else:
                    to_print = [
                        CONFIGURATION["domain"], self.domain_status, self.source
                    ]

                Prints(to_print, "Less", output, True).data()
            else:
                to_print = [
                    CONFIGURATION["domain"],
                    self.domain_status,
                    self.expiration_date,
                    self.source,
                    CONFIGURATION["http_code"],
                    CURRENT_TIME,
                ]

                Prints(to_print, "Generic_File", output, True).data()

    def _analytic_file(self, new_status, old_status):
        """
        Generate HTTP_Analytic/* files.

        Arguments:
            - new_status: str
                The new status of the domain.
            - old_status: str
                The old status of the domain.
        """

        output = self.output_parent_dir + OUTPUTS["http_analytic"]["directories"][
            "parent"
        ] + "%s%s"
        if new_status.lower() in STATUS["list"]["up"]:
            output = output % (
                OUTPUTS["http_analytic"]["directories"]["up"],
                OUTPUTS["http_analytic"]["filenames"]["up"],
            )
            Generate("HTTP_Active").hosts_file()
        elif new_status.lower() in STATUS["list"]["potentially_up"]:
            output = output % (
                OUTPUTS["http_analytic"]["directories"]["potentially_up"],
                OUTPUTS["http_analytic"]["filenames"]["potentially_up"],
            )
            Generate("potentially_up").hosts_file()
        else:
            output = output % (
                OUTPUTS["http_analytic"]["directories"]["potentially_down"],
                OUTPUTS["http_analytic"]["filenames"]["potentially_down"],
            )

        Prints(
            [
                CONFIGURATION["domain"],
                old_status,
                CONFIGURATION["http_code"],
                CURRENT_TIME,
            ],
            "HTTP",
            output,
            True,
        ).data()

    def special_blogspot(self):
        """
        Handle the blogspot SPECIAL case.
        """

        regex_blogspot = ".blogspot."
        regex_blogger = ["create-blog.g?", "87065", "doesn&#8217;t&nbsp;exist"]

        if Helpers.Regex(
            CONFIGURATION["domain"], regex_blogspot, return_data=False, escape=True
        ).match():
            blogger_content_request = requests.get(
                "http://%s:80" % CONFIGURATION["domain"]
            )

            for regx in regex_blogger:
                if regx in blogger_content_request.text or Helpers.Regex(
                    blogger_content_request.text, regx, return_data=False, escape=False
                ).match():
                    self.source = "SPECIAL"
                    self.domain_status = STATUS["official"]["down"]
                    self.output = self.output_parent_dir + OUTPUTS["splited"][
                        "directory"
                    ] + self.domain_status
                    break

    def special_wordpress_com(self):
        """
        Handle the wordpress.com special case.
        """

        wordpress_com = ".wordpress.com"
        does_not_exist = "doesn&#8217;t&nbsp;exist"

        if CONFIGURATION["domain"].endswith(wordpress_com):
            wordpress_com_content = requests.get(
                "http://%s:80" % CONFIGURATION["domain"]
            )

            if does_not_exist in wordpress_com_content.text:
                self.source = "SPECIAL"
                self.domain_status = STATUS["official"]["down"]
                self.output = self.output_parent_dir + OUTPUTS["splited"][
                    "directory"
                ] + self.domain_status

    def up_status_file(self):
        """
        Logic behind the up status when generating the status file.
        """

        if not self.expiration_date:
            self.expiration_date = "Unknown"

        if HTTP_CODE["active"] and CONFIGURATION["http_code"] in HTTP_CODE["list"][
            "potentially_down"
        ]:
            self._analytic_file(STATUS["official"]["down"], self.domain_status)

            regex_to_match = [
                ".canalblog.com",
                ".doubleclick.net",
                ".liveadvert.com",
                ".skyrock.com",
                ".tumblr.com",
            ]

            for regx in regex_to_match:
                if Helpers.Regex(
                    CONFIGURATION["domain"], regx, return_data=False, escape=True
                ).match():
                    self.source = "SPECIAL"
                    self.domain_status = STATUS["official"]["down"]
                    self.output = self.output_parent_dir + OUTPUTS["splited"][
                        "directory"
                    ] + self.domain_status

            self.special_blogspot()
        elif HTTP_CODE["active"] and CONFIGURATION["http_code"] in HTTP_CODE["list"][
            "potentially_up"
        ]:
            self.special_blogspot()
            self.special_wordpress_com()

        if self.source != "SPECIAL":
            self.domain_status = STATUS["official"]["up"]
            self.output = self.output_parent_dir + OUTPUTS["splited"][
                "directory"
            ] + self.domain_status

    def down_status_file(self):
        """
        Logic behind the down status when generating the status file.
        """

        self.refer_status = "Not Found"
        self.expiration_date = "Unknown"

        if HTTP_CODE["active"]:
            if CONFIGURATION["http_code"] in HTTP_CODE["list"]["up"]:
                self._analytic_file(STATUS["official"]["up"], self.domain_status)
                self.source = "HTTP Code"
                self.domain_status = STATUS["official"]["up"]
                self.output = self.output_parent_dir + OUTPUTS["splited"][
                    "directory"
                ] + self.domain_status
            elif CONFIGURATION["http_code"] in HTTP_CODE["list"]["potentially_up"]:
                self._analytic_file("potentially_up", self.domain_status)

        if Helpers.Regex(
            CONFIGURATION["domain"],
            r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[0-9]{1,}\/[0-9]{1,})$",  # pylint: disable=line-too-long
            return_data=False,
        ).match():
            self.source = "SPECIAL"
            self.domain_status = STATUS["official"]["up"]
            self.output = self.output_parent_dir + OUTPUTS["splited"][
                "directory"
            ] + self.domain_status

        if self.source != "HTTP Code" and self.source != "SPECIAL":
            self.domain_status = STATUS["official"]["down"]
            self.output = self.output_parent_dir + OUTPUTS["splited"][
                "directory"
            ] + self.domain_status

    def invalid_status_file(self):
        """
        Logic behind the invalid status when generating the status file.
        """

        self.expiration_date = "Unknown"

        if HTTP_CODE["active"]:
            try:
                if CONFIGURATION["http_code"] in HTTP_CODE["list"]["up"]:
                    self._analytic_file(STATUS["official"]["up"], self.domain_status)
                    self.source = "HTTP Code"
                    self.domain_status = STATUS["official"]["up"]
                    self.output = self.output_parent_dir + OUTPUTS["splited"][
                        "directory"
                    ] + self.domain_status
                elif CONFIGURATION["http_code"] in HTTP_CODE["list"]["potentially_up"]:
                    self._analytic_file("potentially_up", self.domain_status)
                elif CONFIGURATION["http_code"] in HTTP_CODE["list"][
                    "potentially_down"
                ]:
                    self._analytic_file(STATUS["official"]["down"], self.domain_status)
            except KeyError:
                pass

            if self.source != "HTTP Code":
                self.domain_status = STATUS["official"]["invalid"]
                self.output = self.output_parent_dir + OUTPUTS["splited"][
                    "directory"
                ] + self.domain_status

    def _prints_status_file(self):
        """
        Logic behind the printing when generating status file.
        """

        if CONFIGURATION["less"]:
            Prints(
                [CONFIGURATION["domain"], self.domain_status, self.source],
                "Less",
                self.output,
                True,
            ).data()
        else:
            if not CONFIGURATION["split"]:
                if self.domain_status.lower() in STATUS["list"]["up"]:
                    Prints(
                        [
                            CONFIGURATION["domain"],
                            self.expiration_date,
                            self.source,
                            CONFIGURATION["http_code"],
                            CURRENT_TIME,
                        ],
                        STATUS["official"]["up"],
                        self.output,
                        True,
                    ).data()
                elif self.domain_status.lower() in STATUS["list"]["down"]:
                    Prints(
                        [
                            CONFIGURATION["domain"],
                            CONFIGURATION["referer"],
                            self.domain_status,
                            self.source,
                            CONFIGURATION["http_code"],
                            CURRENT_TIME,
                        ],
                        STATUS["official"]["down"],
                        self.output,
                        True,
                    ).data()
                elif self.domain_status.lower() in STATUS["list"]["invalid"]:
                    Prints(
                        [
                            CONFIGURATION["domain"],
                            self.source,
                            CONFIGURATION["http_code"],
                            CURRENT_TIME,
                        ],
                        STATUS["official"]["invalid"],
                        self.output,
                        True,
                    ).data()

    def status_file(self):
        """
        Generate a file according to the domain status.
        """

        try:
            CONFIGURATION["http_code"]
        except KeyError:
            CONFIGURATION["http_code"] = "*" * 3

        if self.domain_status.lower() in STATUS["list"]["up"]:
            self.up_status_file()
        elif self.domain_status.lower() in STATUS["list"]["down"]:
            self.down_status_file()
        elif self.domain_status.lower() in STATUS["list"]["invalid"]:
            self.invalid_status_file()

        Generate(self.domain_status, self.source, self.expiration_date).hosts_file()
        Percentage(self.domain_status).count()

        if not CONFIGURATION["quiet"]:
            if CONFIGURATION["less"]:
                Prints(
                    [
                        CONFIGURATION["domain"],
                        self.domain_status,
                        CONFIGURATION["http_code"],
                    ],
                    "Less",
                ).data()
            else:
                Prints(
                    [
                        CONFIGURATION["domain"],
                        self.domain_status,
                        self.expiration_date,
                        self.source,
                        CONFIGURATION["http_code"],
                    ],
                    "Generic",
                ).data()

        if not CONFIGURATION["no_files"] and CONFIGURATION["split"]:
            self._prints_status_file()
        else:
            self.unified_file()


class Status(object):  # pylint: disable=too-few-public-methods
    """
    Return the domain status in case we don't use WHOIS or in case that WHOIS
    record is not readable.

    Argument:
        - matched_result: str
            The previously catched status.
    """

    def __init__(self, matched_status):
        self.matched_status = matched_status

    def handle(self):
        """
        Handle the lack of WHOIS. :)

        Returns: str
            The status of the domains after generating the files.
        """

        source = "NSLOOKUP"

        if self.matched_status.lower() not in STATUS["list"]["invalid"]:
            if Lookup().nslookup():
                Generate(STATUS["official"]["up"], source).status_file()
                return STATUS["official"]["up"]

            Generate(STATUS["official"]["down"], source).status_file()
            return STATUS["official"]["down"]

        Generate(STATUS["official"]["invalid"], "IANA").status_file()
        return STATUS["official"]["invalid"]


class Referer(object):
    """
    Get the WHOIS server (referer) of the current domain extension according to
        the IANA database.
    """

    def __init__(self):
        self.domain_extension = CONFIGURATION["domain"][
            CONFIGURATION["domain"].rindex(".") + 1:
        ]

        self.ignored_extension = [
            "ad",
            "al",
            "an",
            "ao",
            "aq",
            "arpa",
            "az",
            "ba",
            "bb",
            "bd",
            "bf",
            "bh",
            "bl",
            "bq",
            "bs",
            "bt",
            "bv",
            "cg",
            "ck",
            "cu",
            "cv",
            "cw",
            "cy",
            "dj",
            "doosan",
            "eg",
            "eh",
            "et",
            "fk",
            "flsmidth",
            "fm",
            "gb",
            "gm",
            "gn",
            "gp",
            "gr",
            "gt",
            "gu",
            "gw",
            "htc",
            "iinet",
            "jm",
            "jo",
            "kh",
            "km",
            "kp",
            "lb",
            "lr",
            "mc",
            "mh",
            "mil",
            "mm",
            "mt",
            "mv",
            "mw",
            "ne",
            "ni",
            "np",
            "nr",
            "pa",
            "pg",
            "ph",
            "pk",
            "pn",
            "py",
            "sd",
            "sr",
            "ss",
            "sv",
            "sz",
            "tj",
            "tp",
            "tt",
            "va",
            "vi",
            "vn",
            "ye",
            "zw",
        ]

    @classmethod
    def _iana_database(cls):
        """
        Convert `iana-domains-db.json` into a dictionnary.
        """

        file_to_read = CURRENT_DIRECTORY + OUTPUTS["default_files"]["iana"]

        return Helpers.Dict().from_json(Helpers.File(file_to_read).read())

    def get(self):
        """
        Return the referer aka the WHOIS server of the current domain extension.
        """

        if not CONFIGURATION["no_whois"]:
            if self.domain_extension not in self.ignored_extension:
                referer = None

                if CONFIGURATION["iana_db"] == {}:
                    CONFIGURATION["iana_db"].update(self._iana_database())

                if self.domain_extension in CONFIGURATION["iana_db"]:
                    referer = CONFIGURATION["iana_db"][self.domain_extension]

                    if referer is None:
                        self.log()
                        return Status(STATUS["official"]["down"]).handle()

                    return referer

                return Status(STATUS["official"]["invalid"]).handle()

            return Status(STATUS["official"]["down"]).handle()

        return None

    def log(self):
        """
        Log if no referer is found for a domain extension.
        """

        if CONFIGURATION["logs"]:
            logs = "=" * 100
            logs += "\nNo referer found for: %s domains\n" % self.domain_extension
            logs += "=" * 100
            logs += "\n"

            Helpers.File(
                CURRENT_DIRECTORY
                + OUTPUTS["parent_directory"]
                + OUTPUTS["logs"]["directories"]["parent"]
                + OUTPUTS["logs"]["directories"]["no_referer"]
                + self.domain_extension
            ).write(
                logs
            )

            if CONFIGURATION["share_logs"]:
                data_to_share = {"extension": self.domain_extension}

                requests.post(LINKS["api_no_referer"], data=data_to_share)


class ExpirationDate(object):
    """
    Get, format and return the epiration date of a domain if exist.
    """

    def __init__(self):
        self.log_separator = "=" * 100 + " \n"

        self.expiration_date = ""
        self.whois_record = ""

    @classmethod
    def is_domain_valid(cls, domain=None):
        """
        Check if CONFIGURATION['domain'] is a valid domain.

        Argument:
            - domain: str
                The domain to test

        """

        regex_valid_domains = r"^(?=.{0,253}$)(([a-z0-9][a-z0-9-]{0,61}[a-z0-9]|[a-z0-9])\.)+((?=.*[^0-9])([a-z0-9][a-z0-9-]{0,61}[a-z0-9]|[a-z0-9]))$"  # pylint: disable=line-too-long

        if domain:
            to_test = domain
        else:
            to_test = CONFIGURATION["domain"]

        return Helpers.Regex(to_test, regex_valid_domains, return_data=False).match()

    @classmethod
    def is_ip_valid(cls, IP=None):
        """
        Check if CONFIGURATION['domain'] is a valid IPv4.

        Argument:
            - IP: str
                The ip to test

        Note:
            We only test IPv4 because for now we only support domain and IPv4.
        """

        regex_ipv4 = r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"  # pylint: disable=line-too-long

        if IP:
            to_test = IP
        else:
            to_test = CONFIGURATION["domain"]

        return Helpers.Regex(to_test, regex_ipv4, return_data=False).match()

    def get(self):
        """
        Execute the logic behind the meaning of ExpirationDate + return the matched status.
        """

        domain_validation = self.is_domain_valid()
        ip_validation = self.is_ip_valid()

        if domain_validation and not ip_validation or domain_validation:
            CONFIGURATION.update(
                {"http_code": HTTPCode().get(), "referer": Referer().get()}
            )

            if CONFIGURATION["referer"] in [
                STATUS["official"]["up"],
                STATUS["official"]["down"],
                STATUS["official"]["invalid"],
            ]:
                return CONFIGURATION["referer"]

            elif CONFIGURATION["referer"]:
                return self._extract()

            self._whois_log()
            return Status(STATUS["official"]["down"]).handle()

        elif ip_validation and not domain_validation or ip_validation:
            CONFIGURATION["http_code"] = HTTPCode().get()

            self._whois_log()
            return Status(STATUS["official"]["down"]).handle()

        self._whois_log()
        return Status(STATUS["official"]["invalid"]).handle()

    def _whois_log(self):
        """
        Log the whois record into a file
        """

        if CONFIGURATION["debug"] and CONFIGURATION["logs"]:
            log = self.log_separator + str(
                self.whois_record
            ) + "\n" + self.log_separator

            Helpers.File(
                CURRENT_DIRECTORY
                + OUTPUTS["parent_directory"]
                + OUTPUTS["logs"]["directories"]["parent"]
                + OUTPUTS["logs"]["directories"]["whois"]
                + CONFIGURATION["referer"]
            ).write(
                log
            )

    @classmethod
    def _convert_1_to_2_digits(cls, number):
        """
        Convert 1 digit number to two digits.
        """

        return str(number).zfill(2)

    @classmethod
    def _convert_or_shorten_month(cls, data):
        """
        Convert a given month into our unified format.

        Argument:
            - data: str
                The month to convert or shorten.

        Returns: str
            The unified month name.
        """

        short_month = {
            "jan": [str(1), "01", "Jan", "January"],
            "feb": [str(2), "02", "Feb", "February"],
            "mar": [str(3), "03", "Mar", "March"],
            "apr": [str(4), "04", "Apr", "April"],
            "may": [str(5), "05", "May"],
            "jun": [str(6), "06", "Jun", "June"],
            "jul": [str(7), "07", "Jul", "July"],
            "aug": [str(8), "08", "Aug", "August"],
            "sep": [str(9), "09", "Sep", "September"],
            "oct": [str(10), "Oct", "October"],
            "nov": [str(11), "Nov", "November"],
            "dec": [str(12), "Dec", "December"],
        }

        for month in short_month:
            if data in short_month[month]:
                return month

        return data

    def log(self):
        """
        Log the extracted expiration date and domain into a file.
        """

        if CONFIGURATION["logs"]:
            log = self.log_separator + "Expiration Date: %s \n" % self.expiration_date
            log += "Tested domain: %s \n" % CONFIGURATION["domain"]

            Helpers.File(
                CURRENT_DIRECTORY
                + OUTPUTS["parent_directory"]
                + OUTPUTS["logs"]["directories"]["parent"]
                + OUTPUTS["logs"]["directories"]["date_format"]
                + CONFIGURATION["referer"]
            ).write(
                log
            )

            if CONFIGURATION["share_logs"]:
                date_to_share = {
                    "domain": CONFIGURATION["domain"],
                    "expiration_date": self.expiration_date,
                    "whois_server": CONFIGURATION["referer"],
                }

                requests.post(LINKS["api_date_format"], data=date_to_share)

    @classmethod
    def _cases_management(cls, regex_number, matched_result):
        """
        A little helper of self.format. (Avoiding of nested loops)

        Note:
            Please note that the second value of the case represent the groups
            in order [day,month,year]. This means that a [2,1,0] will be for
            example for a date in format `2017-01-02` where `01` is the month.

        Retuns: list or None
            - None: the case is unknown.
            - list: the list representing the date [day, month, year]
        """

        cases = {
            "first": [[1, 2, 3, 10, 11, 22, 26, 27, 28, 29, 32, 34], [0, 1, 2]],
            "second": [[14, 15, 31, 33, 36, 37], [1, 0, 2]],
            "third": [
                [4, 5, 6, 7, 8, 9, 12, 13, 16, 17, 18, 19, 20, 21, 23, 24, 25, 30, 35],
                [2, 1, 0],
            ],
        }

        for case in cases:
            case_data = cases[case]

            if int(regex_number) in case_data[0]:
                return [
                    matched_result[case_data[1][0]],
                    matched_result[case_data[1][1]],
                    matched_result[case_data[1][2]],
                ]

            else:
                continue

        return None

    def _format(self):
        """
        Format the expiration date into an unified format (01-jan-1970).
        """

        regex_dates = {
            # Date in format: 02-jan-2017
            "1": r"([0-9]{2})-([a-z]{3})-([0-9]{4})",
            # Date in format: 02.01.2017 // Month: jan
            "2": r"([0-9]{2})\.([0-9]{2})\.([0-9]{4})$",
            # Date in format: 02/01/2017 // Month: jan
            "3": r"([0-3][0-9])\/(0[1-9]|1[012])\/([0-9]{4})",
            # Date in format: 2017-01-02 // Month: jan
            "4": r"([0-9]{4})-([0-9]{2})-([0-9]{2})$",
            # Date in format: 2017.01.02 // Month: jan
            "5": r"([0-9]{4})\.([0-9]{2})\.([0-9]{2})$",
            # Date in format: 2017/01/02 // Month: jan
            "6": r"([0-9]{4})\/([0-9]{2})\/([0-9]{2})$",
            # Date in format: 2017.01.02 15:00:00
            "7": r"([0-9]{4})\.([0-9]{2})\.([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}",
            # Date in format: 20170102 15:00:00 // Month: jan
            "8": r"([0-9]{4})([0-9]{2})([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}",
            # Date in format: 2017-01-02 15:00:00 // Month: jan
            "9": r"([0-9]{4})-([0-9]{2})-([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}",
            # Date in format: 02.01.2017 15:00:00 // Month: jan
            "10": r"([0-9]{2})\.([0-9]{2})\.([0-9]{4})\s[0-9]{2}:[0-9]{2}:[0-9]{2}",
            # Date in format: 02-Jan-2017 15:00:00 UTC
            "11": r"([0-9]{2})-([A-Z]{1}[a-z]{2})-([0-9]{4})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s[A-Z]{1}.*",  # pylint: disable=line-too-long
            # Date in format: 2017/01/02 01:00:00 (+0900) // Month: jan
            "12": r"([0-9]{4})\/([0-9]{2})\/([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s\(.*\)",
            # Date in format: 2017/01/02 01:00:00 // Month: jan
            "13": r"([0-9]{4})\/([0-9]{2})\/([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}$",
            # Date in format: Mon Jan 02 15:00:00 GMT 2017
            "14": r"[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s[A-Z]{3}\s([0-9]{4})",  # pylint: disable=line-too-long
            # Date in format: Mon Jan 02 2017
            "15": r"[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{2})\s([0-9]{4})",
            # Date in format: 2017-01-02T15:00:00 // Month: jan
            "16": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}$",
            # Date in format: 2017-01-02T15:00:00Z // Month: jan${'7}
            "17": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}[A-Z].*",
            # Date in format: 2017-01-02T15:00:00+0200 // Month: jan
            "18": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{4}",
            # Date in format: 2017-01-02T15:00:00+0200.622265+03:00 //
            # Month: jan
            "19": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9].*[+-][0-9]{2}:[0-9]{2}",  # pylint: disable=line-too-long
            # Date in format: 2017-01-02T15:00:00+0200.622265 // Month: jan
            "20": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}$",
            # Date in format: 2017-01-02T23:59:59.0Z // Month: jan
            "21": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9].*[A-Z]",
            # Date in format: 02-01-2017 // Month: jan
            "22": r"([0-9]{2})-([0-9]{2})-([0-9]{4})",
            # Date in format: 2017. 01. 02. // Month: jan
            "23": r"([0-9]{4})\.\s([0-9]{2})\.\s([0-9]{2})\.",
            # Date in format: 2017-01-02T00:00:00+13:00 // Month: jan
            "24": r"([0-9]{4})-([0-9]{2})-([0-9]{2})T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}",  # pylint: disable=line-too-long
            # Date in format: 20170102 // Month: jan
            "25": r"(?=[0-9]{8})(?=([0-9]{4})([0-9]{2})([0-9]{2}))",
            # Date in format: 02-Jan-2017
            "26": r"([0-9]{2})-([A-Z]{1}[a-z]{2})-([0-9]{4})$",
            # Date in format: 02.1.2017 // Month: jan
            "27": r"([0-9]{2})\.([0-9]{1})\.([0-9]{4})",
            # Date in format: 02 Jan 2017
            "28": r"([0-9]{1,2})\s([A-Z]{1}[a-z]{2})\s([0-9]{4})",
            # Date in format: 02-January-2017
            "29": r"([0-9]{2})-([A-Z]{1}[a-z]*)-([0-9]{4})",
            # Date in format: 2017-Jan-02.
            "30": r"([0-9]{4})-([A-Z]{1}[a-z]{2})-([0-9]{2})\.",
            # Date in format: Mon Jan 02 15:00:00 2017
            "31": r"[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{1,2})\s[0-9]{2}:[0-9]{2}:[0-9]{2}\s([0-9]{4})",  # pylint: disable=line-too-long
            # Date in format: Mon Jan 2017 15:00:00
            "32": r"()[a-zA-Z]{3}\s([a-zA-Z]{3})\s([0-9]{4})\s[0-9]{2}:[0-9]{2}:[0-9]{2}",
            # Date in format: January 02 2017-Jan-02
            "33": r"([A-Z]{1}[a-z]*)\s([0-9]{1,2})\s([0-9]{4})",
            # Date in format: 2.1.2017 // Month: jan
            "34": r"([0-9]{1,2})\.([0-9]{1,2})\.([0-9]{4})",
            # Date in format: 20170102000000 // Month: jan
            "35": r"([0-9]{4})([0-9]{2})([0-9]{2})[0-9]+",
            # Date in format: 01/02/2017 // Month: jan
            "36": r"(0[1-9]|1[012])\/([0-3][0-9])\/([0-9]{4})",
            # Date in format: January  1 2017
            "37": r"([A-Z]{1}[a-z].*)\s\s([0-9]{1,2})\s([0-9]{4})",
        }

        for regx in regex_dates:
            matched_result = Helpers.Regex(
                self.expiration_date, regex_dates[regx], return_data=True, rematch=True
            ).match()

            if matched_result:
                date = self._cases_management(regx, matched_result)

                if date:
                    day = self._convert_1_to_2_digits(date[0])
                    month = self._convert_or_shorten_month(date[1])
                    year = str(date[2])

                    self.expiration_date = day + "-" + month + "-" + year
                break

        if self.expiration_date and not Helpers.Regex(
            self.expiration_date, r"[0-9]{2}\-[a-z]{3}\-2[0-9]{3}", return_data=False
        ).match():
            self.log()
            self._whois_log()

    def _extract(self):
        """
        Extract the expiration date from the whois record.
        """

        self.whois_record = Lookup().whois(CONFIGURATION["referer"])

        to_match = [
            r"expire:(.*)",
            r"expire on:(.*)",
            r"Expiry Date:(.*)",
            r"free-date(.*)",
            r"expires:(.*)",
            r"Expiration date:(.*)",
            r"Expiry date:(.*)",
            r"Expire Date:(.*)",
            r"renewal date:(.*)",
            r"Expires:(.*)",
            r"validity:(.*)",
            r"Expiration Date             :(.*)",
            r"Expiry :(.*)",
            r"expires at:(.*)",
            r"domain_datebilleduntil:(.*)",
            r"Data de expiração \/ Expiration Date \(dd\/mm\/yyyy\):(.*)",
            r"Fecha de expiración \(Expiration date\):(.*)",
            r"\[Expires on\](.*)",
            r"Record expires on(.*)(\(YYYY-MM-DD\))",
            r"status:      OK-UNTIL(.*)",
            r"renewal:(.*)",
            r"expires............:(.*)",
            r"expire-date:(.*)",
            r"Exp date:(.*)",
            r"Valid-date(.*)",
            r"Expires On:(.*)",
            r"Fecha de vencimiento:(.*)",
            r"Expiration:.........(.*)",
            r"Fecha de Vencimiento:(.*)",
            r"Registry Expiry Date:(.*)",
            r"Expires on..............:(.*)",
            r"Expiration Time:(.*)",
            r"Expiration Date:(.*)",
            r"Expired:(.*)",
            r"Date d'expiration:(.*)",
        ]

        if self.whois_record:
            for string in to_match:
                expiration_date = Helpers.Regex(
                    self.whois_record, string, return_data=True, rematch=True, group=0
                ).match()

                if expiration_date:
                    self.expiration_date = expiration_date[0].strip()

                    regex_rumbers = r"[0-9]"
                    if Helpers.Regex(
                        self.expiration_date, regex_rumbers, return_data=False
                    ).match():

                        self._format()
                        Generate(
                            STATUS["official"]["up"], "WHOIS", self.expiration_date
                        ).status_file()

                        self._whois_log()
                        return STATUS["official"]["up"]

                    self._whois_log()
                    return Status(STATUS["official"]["down"]).handle()

        self._whois_log()
        return Status(STATUS["official"]["down"]).handle()


class IANA(object):
    """
    Logic behind the update of `iana-domains-db.json`
    """

    def __init__(self):
        if not CONFIGURATION["quiet"]:
            print("Update of iana-domains-db", end=" ")

        self.destination = OUTPUTS["default_files"]["iana"]
        self.iana_db = {}

        self.update()

    @classmethod
    def data(cls):
        """
        Get the database from IANA website.
        """
        iana_url = "https://www.iana.org/domains/root/db"

        req = requests.get(iana_url)

        return req.text

    @classmethod
    def referer(cls, extension):
        """
        Return the referer for the given extension.

        :pram extension: A string, a valid domain extension.
        """

        manual_server = {
            "aaa": "whois.nic.aaa",
            "abb": "whois.nic.abb",
            "able": "whois.nic.able",
            "accenture": "whois.nic.accenture",
            "aetna": "whois.nic.aetna",
            "aig": "whois.nic.aig",
            "americanexpress": "whois.nic.americanexpress",
            "amex": "whois.nic.amex",
            "amica": "whois.nic.amica",
            "amsterdam": "whois.nic.amsterdam",
            "analytics": "whois.nic.analytics",
            "aramco": "whois.nic.aramco",
            "athleta": "whois.nic.athleta",
            "audible": "whois.nic.audible",
            "author": "whois.nic.author",
            "aws": "whois.nic.aws",
            "axa": "whois.nic.axa",
            "azure": "whois.nic.azure",
            "baby": "whois.nic.baby",
            "banamex": "whois.nic.banamex",
            "bananarepublic": "whois.nic.bananarepublic",
            "baseball": "whois.nic.baseball",
            "bharti": "whois.nic.bharti",
            "bing": "whois.nic.bing",
            "bloomberg": "whois.nic.bloomberg",
            "bm": "whois.afilias-srs.net",
            "book": "whois.nic.book",
            "booking": "whois.nic.booking",
            "bot": "whois.nic.bot",
            "bz": "whois.afilias-grs.net",
            "buzz": "whois.nic.buzz",
            "call": "whois.nic.call",
            "calvinklein": "whois.nic.calvinklein",
            "caravan": "whois.nic.caravan",
            "cartier": "whois.nic.cartier",
            "cbn": "whois.nic.cbn",
            "cbre": "whois.nic.cbre",
            "cd": "chois.nic.cd",
            "chase": "whois.nic.chase",
            "circle": "whois.nic.circle",
            "cisco": "whois.nic.cisco",
            "citadel": "whois.nic.citadel",
            "citi": "whois.nic.citi",
            "citic": "whois.nic.citic",
            "cm": "whois.netcom.cm",
            "coupon": "whois.nic.coupon",
            "crown": "whois.nic.crown",
            "crs": "whois.nic.crs",
            "deal": "whois.nic.deal",
            "dealer": "whois.nic.dealer",
            "dell": "whois.nic.dell",
            "dhl": "whois.nic.dhl",
            "discover": "whois.nic.discover",
            "dnp": "whois.nic.dnp",
            "duns": "whois.nic.duns",
            "dupont": "whois.nic.dupont",
            "earth": "whois.nic.earth",
            "epost": "whois.nic.epost",
            "everbank": "whois.nic.everbank",
            "farmers": "whois.nic.farmers",
            "fast": "whois.nic.fast",
            "ferrero": "whois.nic.ferrero",
            "fire": "whois.nic.fire",
            "fj": "whois.usp.ac.fj",
            "flickr": "whois.nic.flickr",
            "flir": "whois.nic.flir",
            "food": "whois.nic.food",
            "ford": "whois.nic.ford",
            "fox": "whois.nic.fox",
            "free": "whois.nic.free",
            "frontier": "whois.nic.frontier",
            "ftr": "whois.nic.ftr",
            "ga": "whois.my.ga",
            "gap": "whois.nic.gap",
            "gh": "whois.nic.gh",
            "gmo": "whois.nic.gmo",
            "got": "whois.nic.got",
            "grainger": "whois.nic.grainger",
            "grocery": "whois.nic.grocery",
            "guardian": "whois.nic.guardian",
            "gucci": "whois.nic.gucci",
            "hair": "whois.nic.hair",
            "hbo": "whois.nic.hbo",
            "health": "whois.nic.health",
            "homegoods": "whois.nic.homegoods",
            "homesense": "whois.nic.homesense",
            "honeywell": "whois.nic.honeywell",
            "hoteles": "whois.nic.hoteles",
            "hotels": "whois.nic.hotels",
            "hotmail": "whois.nic.hotmail",
            "hyatt": "whois.nic.hyatt",
            "hsbc": "whois.nic.hsbc",
            "hot": "whois.nic.hot",
            "ieee": "whois.nic.ieee",
            "imdb": "whois.nic.imdb",
            "int": "whois.iana.org",
            "intel": "whois.nic.intel",
            "intuit": "whois.nic.intuit",
            "ipirange": "whois.nic.ipiranga",
            "itau": "whois.nic.itau",
            "iwc": "whois.nic.iwc",
            "jetzt": "whois.nic.jetzt",
            "jlc": "whois.nic.jlc",
            "jmp": "whois.nic.jmp",
            "jnj": "whois.nic.jnj",
            "jot": "whois.nic.jot",
            "joy": "whois.nic.joy",
            "jpmorgan": "whois.nic.jpmorgan",
            "jprs": "whois.nic.jprs",
            "kinder": "whois.nic.kinder",
            "kindle": "whois.nic.kindle",
            "kpmg": "whois.nic.kpmg",
            "kpn": "whois.nic.kpn",
            "kred": "whois.nic.kred",
            "kw": "whois.nic.kw",
            "lanxess": "whois.nic.lanxess",
            "lifeinsurance": "whois.nic.lifeinsurance",
            "like": "whois.nic.like",
            "lc": "whois2.afilias-grs.net",
            "lk": "whois.nic.lk",
            "microsoft": "whois.nic.microsoft",
            "nagoya": "whois.nic.nagoya",
            "nyc": "whois.nic.nyc",
            "ps": "whois.pnina.ps",
            "ren": "whois.nic.ren",
            "rw": "whois.ricta.org.rw",
            "shop": "whois.nic.shop",
            "sl": "whois.nic.sl",
            "stream": "whois.nic.stream",
            "tokyo": "whois.nic.tokyo",
            "uno": "whois.nic.uno",
            "za": "whois.registry.net.za",
        }

        if extension in manual_server:
            return manual_server[extension]

        else:
            whois_record = Lookup().whois(
                CONFIGURATION["iana_whois_server"], "hello." + extension, 10
            )

            if whois_record:
                regex_referer = r"(refer:)\s+(.*)"

                matched = Helpers.Regex(
                    whois_record, regex_referer, return_data=True, rematch=True
                ).match()

                if matched:
                    return matched[1]

            return None

    def _extensions(self, line):
        """
        Extract the extention from the given line.
        Plus get its referer.

        Argument:
            - line: str
                The line from self.iana_url.
        """

        regex_valid_extension = r"(/domains/root/db/)(.*)(\.html)"

        if "/domains/root/db/" in line:
            matched = Helpers.Regex(
                line, regex_valid_extension, return_data=True, rematch=True
            ).match()[
                1
            ]

            if matched:
                self.iana_db.update({matched: self.referer(matched)})

    def update(self):
        """
        Update the content of the `iana-domains-db` file.
        """

        list(map(self._extensions, self.data().split("\n")))
        Helpers.Dict(self.iana_db).to_json(self.destination)

        if not CONFIGURATION["quiet"]:
            print(CONFIGURATION["done"])


class DirectoryStructure(object):
    """
    Consider this class as a backup/reconstructor of desired directory.
    (By default, the output direcctory)
    """

    def __init__(self, production=False):
        if OUTPUTS["main"]:
            self.base = OUTPUTS["main"]
        else:
            self.base = CURRENT_DIRECTORY

        if not self.base.endswith(directory_separator):
            self.base += directory_separator

        self.structure = self.base + OUTPUTS["default_files"]["dir_structure"]

        if production:
            self.backup()
        else:
            self.restore()

    @classmethod
    def backup(cls):
        """
        Backup the developer state of `output/` in order to make it restorable
            and portable for user.
        """

        output_path = CURRENT_DIRECTORY + OUTPUTS["parent_directory"]
        result = {OUTPUTS["parent_directory"]: {}}

        for root, _, files in walk(output_path):
            directories = root.split(output_path)[1]

            local_result = result[OUTPUTS["parent_directory"]]

            for file in files:
                file_path = root + directory_separator + file
                file_hash = Helpers.Hash(file_path, "sha512", True).get()

                lines_in_list = [line.rstrip("\n") for line in open(file_path)]

                formated_content = "@@@".join(lines_in_list)

                local_result = local_result.setdefault(
                    directories,
                    {file: {"sha512": file_hash, "content": formated_content}},
                )

        Helpers.Dict(result).to_json(
            CURRENT_DIRECTORY + "dir_structure_production.json"
        )

    def _restore_replace(self):
        """
        Check if we need to replace ".gitignore" to ".keep".
        """

        if path.isdir(self.base + ".git"):
            if "PyFunceble" not in Helpers.Command("git remote show origin").execute():
                return True

            return False

        return True

    def _update_structure_from_config(self, structure):
        """
        This method update the paths according to configs.

        Argument:
            - structure: dict
                The readed structure.
        """

        to_replace_base = {"output/": OUTPUTS["parent_directory"]}

        to_replace = {
            "HTTP_Analytic": OUTPUTS["http_analytic"]["directories"]["parent"],
            "HTTP_Analytic/ACTIVE": OUTPUTS["http_analytic"]["directories"]["parent"]
            + OUTPUTS["http_analytic"]["directories"]["up"],
            "HTTP_Analytic/POTENTIALLY_ACTIVE": OUTPUTS["http_analytic"]["directories"][
                "parent"
            ]
            + OUTPUTS["http_analytic"]["directories"]["potentially_up"],
            "HTTP_Analytic/POTENTIALLY_INACTIVE": OUTPUTS["http_analytic"][
                "directories"
            ][
                "parent"
            ]
            + OUTPUTS["http_analytic"]["directories"]["potentially_down"],
            "domains": OUTPUTS["domains"]["directory"],
            "domains/ACTIVE": OUTPUTS["domains"]["directory"]
            + STATUS["official"]["up"]
            + directory_separator,
            "domains/INACTIVE": OUTPUTS["domains"]["directory"]
            + STATUS["official"]["down"]
            + directory_separator,
            "domains/INVALID": OUTPUTS["domains"]["directory"]
            + STATUS["official"]["invalid"]
            + directory_separator,
            "hosts": OUTPUTS["hosts"]["directory"],
            "hosts/ACTIVE": OUTPUTS["hosts"]["directory"]
            + STATUS["official"]["up"]
            + directory_separator,
            "hosts/INACTIVE": OUTPUTS["hosts"]["directory"]
            + STATUS["official"]["down"]
            + directory_separator,
            "hosts/INVALID": OUTPUTS["hosts"]["directory"]
            + STATUS["official"]["invalid"]
            + directory_separator,
            "logs": OUTPUTS["logs"]["directories"]["parent"],
            "logs/date_format": OUTPUTS["logs"]["directories"]["parent"]
            + OUTPUTS["logs"]["directories"]["date_format"],
            "logs/no_referer": OUTPUTS["logs"]["directories"]["parent"]
            + OUTPUTS["logs"]["directories"]["no_referer"],
            "logs/percentage": OUTPUTS["logs"]["directories"]["parent"]
            + OUTPUTS["logs"]["directories"]["percentage"],
            "logs/whois": OUTPUTS["logs"]["directories"]["parent"]
            + OUTPUTS["logs"]["directories"]["whois"],
            "splited": OUTPUTS["splited"]["directory"],
        }

        structure = Helpers.Dict(structure).rename_key(to_replace_base)
        structure[OUTPUTS["parent_directory"]] = Helpers.Dict(
            structure[OUTPUTS["parent_directory"]]
        ).rename_key(
            to_replace
        )

        try:
            Helpers.Dict(structure).to_json(self.structure)
        except FileNotFoundError:
            mkdir(
                directory_separator.join(self.structure.split(directory_separator)[:-1])
            )
            Helpers.Dict(structure).to_json(self.structure)

        return structure

    def _get_structure(self):
        """
        This method return the structure we are goinng to work with.
        """

        structure_file = ""
        req = ""

        if path.isfile(self.structure):
            structure_file = self.structure
        elif path.isfile(self.base + "dir_structure_production.json"):
            structure_file = self.base + "dir_structure_production.json"
        else:
            try:
                if CONFIGURATION["stable"]:
                    req = requests.get(LINKS["dir_structure"])
            except KeyError:
                req = requests.get(LINKS["dir_structure"].replace("master", "dev"))

        if structure_file.endswith("_production.json"):
            structure = Helpers.Dict().from_json(Helpers.File(structure_file).read())

            return self._update_structure_from_config(structure)

        elif structure_file.endswith(".json"):
            return Helpers.Dict().from_json(Helpers.File(structure_file).read())

        return self._update_structure_from_config(Helpers.Dict().from_json(req.text))

    @classmethod
    def _create_directory(cls, directory):
        """
        This method create the given directory if it does not exists.
        """

        if not path.isdir(directory):
            AutoSave.travis_permissions()
            mkdir(directory)
            AutoSave.travis_permissions()

    def restore(self):
        """
        Restore the 'output/' directory structure based on the `dir_structure.json` file.
        """

        structure = self._get_structure()

        list_of_key = list(structure.keys())
        structure = structure[list_of_key[0]]
        parent_path = list_of_key[0] + directory_separator

        for directory in structure:
            base = self.base + parent_path + directory + directory_separator

            self._create_directory(base)

            for file in structure[directory]:
                file_path = base + file

                content_to_write = structure[directory][file]["content"]
                online_sha = structure[directory][file]["sha512"]

                content_to_write = Helpers.Regex(
                    content_to_write, "@@@", escape=True, replace_with="\\n"
                ).replace()

                git_to_keep = file_path.replace("gitignore", "keep")
                keep_to_git = file_path.replace("keep", "gitignore")

                if self._restore_replace():
                    if path.isfile(file_path) and Helpers.Hash(
                        file_path, "sha512", True
                    ).get() == online_sha:
                        rename(file_path, git_to_keep)
                        write = False
                    else:
                        Helpers.File(file_path).delete()
                        file_path = git_to_keep
                        write = True
                else:
                    if path.isfile(keep_to_git) and Helpers.Hash(
                        file_path, "sha512", True
                    ).get() == online_sha:
                        rename(file_path, keep_to_git)
                        write = False
                    else:
                        Helpers.File(keep_to_git).delete()
                        file_path = keep_to_git
                        write = True

                if write:
                    Helpers.File(file_path).write(content_to_write + "\n", True)


class Update(object):
    """
    Update logic
    """

    def __init__(self, path_update=False):
        self.destination = CURRENT_DIRECTORY + "funilrys."
        self.files = {
            "script": "PyFunceble.py",
            "iana": OUTPUTS["default_files"]["iana"],
            "dir_structure": "dir_structure_production.json",
            "config": "config_production.yaml",
            "requirements": "requirements.txt",
        }

        self.path_update = path_update

        if self.path_update:
            self.files = Helpers.Dict(self.files).remove_key(["script", "requirements"])

        if path.isdir(CURRENT_DIRECTORY + ".git") and "PyFunceble" in Helpers.Command(
            "git remote show origin"
        ).execute():
            self.git()
        else:
            if not self.same_version(True):
                for data in self.files:
                    Helpers.File(CURRENT_DIRECTORY + self.files[data]).delete()
                    rename(
                        self.destination + self.files[data],
                        CURRENT_DIRECTORY + self.files[data],
                    )

                if not CONFIGURATION["quiet"]:
                    print("Checking version", end=" ")
                if self.same_version() and not CONFIGURATION["quiet"]:
                    print(
                        CONFIGURATION["done"]
                        + "\n\nThe update was successfully completed!"
                    )
                else:
                    if not CONFIGURATION["quiet"]:
                        print(
                            CONFIGURATION["error"]
                            + "\nImpossible to update PyFunceble. Please report issue."
                        )
            else:
                if not CONFIGURATION["quiet"]:
                    print("No need to update.\n")

                for data in self.files:
                    Helpers.File(self.destination + self.files[data]).delete()

    @classmethod
    def git(cls):
        """
        Update repository if cloned (git).
        """

        if CONFIGURATION["stable"]:
            Helpers.Command("git checkout master && git stash").execute()
        else:
            Helpers.Command("git checkout dev && git stash").execute()

        print(Helpers.Command("git pull").execute())

    def update_permission(self):
        """
        Update the permissions of the downloaded files in order to be
        executable.
        """

        for data in self.files:
            if data not in ["iana", "dir_structure", "config", "requirements"]:
                try:
                    stats = stat(CURRENT_DIRECTORY + self.files[data])
                    chmod(CURRENT_DIRECTORY + self.files[data], stats.st_mode | S_IEXEC)
                except FileNotFoundError:
                    pass

    def download_files(self):
        """
        Download the online version of PyFunceble and tool.
        """

        if not CONFIGURATION["quiet"] or self.path_update:
            print("\n Download of the scripts ")

        result = []

        for data in self.files:
            if "stable" in CONFIGURATION and CONFIGURATION["stable"]:
                link_to_get = LINKS[data]
            else:
                link_to_get = LINKS[data].replace("master", "dev")

            req = requests.get(link_to_get)

            if req.status_code == 200:
                Helpers.File(self.destination + self.files[data]).write(
                    req.text, overwrite=True
                )
                result.append(True)
            else:
                result.append(False)

        if False not in result:
            self.update_permission()
            return

        if not CONFIGURATION["quiet"] or self.path_update:
            print(
                CONFIGURATION["done"]
                + "\nImpossible to update PyFunceble.py. Please report issue."
            )
            exit(1)

    @classmethod
    def hash(cls, file):
        """
        Get/return the sha512sum of the current PyFunceble.py.

        Argument:
            - file: str
                The file to get the hash.
        """

        return Helpers.Hash(file, "sha512", True).get()

    def same_version(self, download=False):
        """
        Compare the current version to the online version.
        """

        if download:
            self.download_files()

        result = []

        for file in self.files:
            current_version = self.hash(CURRENT_DIRECTORY + self.files[file])
            copied_version = self.hash(self.destination + self.files[file])

            if copied_version is not None:
                if not download and current_version == copied_version:
                    result.append(True)
                else:
                    result.append(False)
            else:
                result.append(True)

        if True in result:
            return True

        return False


class Helpers(object):  # pylint: disable=too-few-public-methods
    """
    PyFunceble's helpers.
    """

    class Hash(object):
        """
        Get and return the hash a file with the given algorithm.

        Arguments:
            - file_path: str
                - The path to the file we have to hash.
            - algorithm: str
                The algoritm to use.
            - only_hash: bool
                True: Return only the desired algorithm

        Note:
            Original version : https://git.io/vFQrK
        """

        def __init__(self, file_path, algorithm="sha512", only_hash=False):
            self.valid_algorithms = ["all", "md5", "sha1", "sha224", "sha384", "sha512"]

            self.path = file_path
            self.algorithm = algorithm
            self.only_hash = only_hash

        def hash_data(self, algo):
            """Get the hash of the given file

            :param algo: A string, the algorithm to use.
            """

            hash_data = getattr(hashlib, algo)()

            with open(self.path, "rb") as file:
                content = file.read()

                hash_data.update(content)
            return hash_data.hexdigest()

        def get(self):
            """
            Return the hash of the given file
            """

            result = {}

            if path.isfile(self.path) and self.algorithm in self.valid_algorithms:
                if self.algorithm == "all":
                    del self.valid_algorithms[0]
                    for algo in self.valid_algorithms:
                        result[algo] = None
                        result[algo] = self.hash_data(algo)
                else:
                    result[self.algorithm] = None
                    result[self.algorithm] = self.hash_data(self.algorithm)
            else:
                return None

            if self.algorithm != "all" and self.only_hash:
                return result[self.algorithm]

            return result

    class Command(object):
        """
        Shell command execution.
        """

        def __init__(self, command):
            self.decode_type = "utf-8"
            self.command = command

        def decode_output(self, to_decode):
            """
            Decode the output of a shell command in order to be readable.

            Argument:
                - to_decode: byte
                    Output of a command to decode.

            Retunes: str
                The decoded output.
            """

            return to_decode.decode(self.decode_type)

        def execute(self):
            """
            Execute the given command.

            Returns: byte
                The output in byte format.
            """

            process = Popen(self.command, stdout=PIPE, stderr=PIPE, shell=True)
            (output, error) = process.communicate()

            if process.returncode != 0:
                return self.decode_output(error)

            return self.decode_output(output)

    class Dict(object):
        """
        Dictionary manipulations.
        """

        def __init__(self, main_dictionnary=None):

            if main_dictionnary is None:
                self.main_dictionnary = {}
            else:
                self.main_dictionnary = main_dictionnary

        def remove_key(self, key_to_remove):
            """
            Remove a given key from a given dictionary.

            Argument:
                - key_to_remove: str or list
                    The key(s) to delete.

            Returns: None or dict
                - None: no dict passed to the class.
                - dict: The dict without the removed key(s).
            """

            if isinstance(self.main_dictionnary, dict):
                if isinstance(key_to_remove, list):
                    for k in key_to_remove:
                        del self.main_dictionnary[k]
                else:
                    del self.main_dictionnary[key_to_remove]
                return self.main_dictionnary

            return None

        def rename_key(self, key_to_rename, strict=True):
            """
            Rename the given keys from the given dictionary.

            Argument:
                - key_to_remove: dict
                    The key(s) to rename.
                    Format: {old:new}
                - strict: bool
                    True: We replace the exact string
                    False: We replace if the string is like.
            """

            if isinstance(self.main_dictionnary, dict) and isinstance(
                key_to_rename, dict
            ):
                for old, new in key_to_rename.items():
                    if strict:
                        self.main_dictionnary[new] = self.main_dictionnary.pop(old)
                    else:
                        to_rename = {}
                        for index in self.main_dictionnary:
                            if old in index:
                                to_rename.update(
                                    {index: new[:-1] + index.split(old)[-1]}
                                )
                        self.main_dictionnary = Helpers.Dict(
                            self.main_dictionnary
                        ).rename_key(
                            to_rename, True
                        )
                return self.main_dictionnary

            return None

        def to_json(self, destination):
            """
            Save a dictionnary into a JSON file.

            Argument:
                - destination: str
                    A path to a file where we're going to
                    write the converted dict into a JSON format.
            """

            with open(destination, "w") as file:
                dump(
                    self.main_dictionnary,
                    file,
                    ensure_ascii=False,
                    indent=4,
                    sort_keys=True,
                )

        @classmethod
        def from_json(cls, data):
            """
            Convert a JSON formated string into a dictionary.

            Argument:
                - data: str
                    A JSON formated string to convert to dict format.
            """

            try:
                return loads(data)

            except decoder.JSONDecodeError:
                return {}

        @classmethod
        def from_yaml(cls, data):
            """
            Convert a YAML formated string into a dictionary.

            Argument:
                - data: str
                    A YAML formated string to convert to dict format.
            """

            return load_yaml(data)

    class Directory(object):  # pylint: disable=too-few-public-methods
        """
        Directory manipulation.

        Argument:
            - directory:str
                A path to the directory to manipulate.
        """

        def __init__(self, directory):
            self.directory = directory

        def fix_path(self):
            """
            This method fix the path of the given path.
            """

            split_path = []
            if self.directory:
                if self.directory.startswith("/") or self.directory.startswith("\\"):
                    if "/" in self.directory:
                        split_path = self.directory[1:].split("/")
                    elif "\\" in self.directory:
                        split_path = self.directory[1:].split("\\")

                    if split_path:
                        return directory_separator.join(split_path)

                if not self.directory.endswith(directory_separator):
                    return self.directory + directory_separator

            return self.directory

    class File(object):
        """
        File treatment/manipulations.

        Argument:
            file: str
                A path to the file to manipulate.
        """

        def __init__(self, file):
            self.file = file

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

        def read(self):
            """
            Read a given file path and return its content.

            Returns: str
                The content of the given file path.
            """

            with open(self.file, "r", encoding="utf-8") as file:
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

    class List(object):  # pylint: disable=too-few-public-methods
        """
        List manipulation.

        Argument:
            - main_list: list
                The list to manipulate.
        """

        def __init__(self, main_list=None):
            if main_list is None:
                self.main_list = []
            else:
                self.main_list = main_list

        def format(self):
            """
            Return a well formated list. Basicaly, it's sort a list and remove duplicate.

            Returns: list
                A sorted, without duplicate, list.
            """

            try:
                return sorted(list(set(self.main_list)), key=str.lower)

            except TypeError:
                return self.main_list

    class Regex(object):  # pylint: disable=too-few-public-methods

        """A simple implementation ot the python.re package

        Arguments:
            - data: str
                The data to regex check.
            - regex: str
                The regex to match.
            - group: int
                The group to return
            - rematch: bool
                True: return the matched groups into a formated list.
                    (implementation of Bash ${BASH_REMATCH})
            - replace_with: str
                The value to replace the matched regex with.
            - occurences: int
                The number of occurence(s) to replace.
        """

        def __init__(self, data, regex, **args):
            # We initiate the needed variable in order to be usable all over
            # class
            self.data = data

            # We assign the default value of our optional arguments
            optional_arguments = {
                "escape": False,
                "group": 0,
                "occurences": 0,
                "rematch": False,
                "replace_with": None,
                "return_data": True,
            }

            # We initiate our optional_arguments in order to be usable all over the
            # class
            for (arg, default) in optional_arguments.items():
                setattr(self, arg, args.get(arg, default))

            if self.escape:  # pylint: disable=no-member
                self.regex = escape(regex)
            else:
                self.regex = regex

        def not_matching_list(self):
            """
            This method return a list of string which don't match the
            given regex.
            """

            pre_result = comp(self.regex)

            return list(
                filter(lambda element: not pre_result.search(str(element)), self.data)
            )

        def matching_list(self):
            """
            This method return a list of the string which match the given
            regex.
            """

            pre_result = comp(self.regex)

            return list(
                filter(lambda element: pre_result.search(str(element)), self.data)
            )

        def match(self):
            """
            Used to get exploitable result of re.search
            """

            # We initate this variable which gonna contain the returned data
            result = []

            # We compile the regex string
            to_match = comp(self.regex)

            # In case we have to use the implementation of ${BASH_REMATCH} we use
            # re.findall otherwise, we use re.search
            if self.rematch:  # pylint: disable=no-member
                pre_result = to_match.findall(self.data)
            else:
                pre_result = to_match.search(self.data)

            if self.return_data and pre_result:  # pylint: disable=no-member
                if self.rematch:  # pylint: disable=no-member
                    for data in pre_result:
                        if isinstance(data, tuple):
                            result.extend(list(data))
                        else:
                            result.append(data)

                    if self.group != 0:  # pylint: disable=no-member
                        return result[self.group]  # pylint: disable=no-member

                else:
                    result = pre_result.group(
                        self.group  # pylint: disable=no-member
                    ).strip()

                return result

            elif not self.return_data and pre_result:  # pylint: disable=no-member
                return True

            return False

        def replace(self):
            """
            Used to replace a matched string with another.
            """

            if self.replace_with:  # pylint: disable=no-member
                return substrings(
                    self.regex,
                    self.replace_with,  # pylint: disable=no-member
                    self.data,
                    self.occurences,  # pylint: disable=no-member
                )

            return self.data


CURRENT_DIRECTORY = directory_separator.join(
    path.abspath(getsourcefile(lambda: 17)).split(directory_separator)[:-1]
) + directory_separator

CONFIGURATION = {}
CURRENT_TIME = strftime("%a %d %b %H:%m:%S %Z %Y")
STATUS = {}
OUTPUTS = {}
HTTP_CODE = {}
LINKS = {}

PYFUNCEBLE_LOGO = """
██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝
"""


def load_configuration(path_to_config):
    """
    This function will load config.yaml and update CONFIGURATION

    Argument:
        - path_to_config: str
            The path to the config.yaml to read.
    """

    if not path_to_config.endswith(directory_separator):
        path_to_config += directory_separator

    CONFIGURATION.update(
        Helpers.Dict.from_yaml(Helpers.File(path_to_config + "config.yaml").read())
    )

    for main_key in ["domains", "hosts", "splited"]:
        CONFIGURATION["outputs"][main_key]["directory"] = Helpers.Directory(
            CONFIGURATION["outputs"][main_key]["directory"]
        ).fix_path()

    for main_key in ["http_analytic", "logs"]:
        for key, value in CONFIGURATION["outputs"][main_key]["directories"].items():
            CONFIGURATION["outputs"][main_key]["directories"][key] = Helpers.Directory(
                value
            ).fix_path()

    CONFIGURATION["outputs"]["main"] = Helpers.Directory(
        CONFIGURATION["outputs"]["main"]
    ).fix_path()

    STATUS.update(CONFIGURATION["status"])
    OUTPUTS.update(CONFIGURATION["outputs"])
    HTTP_CODE.update(CONFIGURATION["http_codes"])
    LINKS.update(CONFIGURATION["links"])

    CONFIGURATION.update({"done": Fore.GREEN + "✔", "error": Fore.RED + "✘"})

    return True


load_configuration(CURRENT_DIRECTORY)

if OUTPUTS["main"]:
    CURRENT_DIRECTORY = OUTPUTS["main"]

    if not CURRENT_DIRECTORY.endswith(directory_separator):
        CURRENT_DIRECTORY += directory_separator

    if not path.isfile(CURRENT_DIRECTORY + OUTPUTS["default_files"]["iana"]):
        Update(path_update=True)

    if path.isfile(CURRENT_DIRECTORY + "config.yaml"):
        load_configuration(CURRENT_DIRECTORY)


if not path.isdir(CURRENT_DIRECTORY + OUTPUTS["parent_directory"]):
    DirectoryStructure()

if __name__ == "__main__":
    initiate(autoreset=True)

    PARSER = argparse.ArgumentParser(
        description='A tool to check domains or IP availability \
        (ACTIVE, INACTIVE, INVALID). Also described as "[an] excellent \
        script for checking ACTIVE and INACTIVE domain names"',
        epilog="Crafted with %s by %s"
        % (
            Fore.RED + "♥" + Fore.RESET,
            Style.BRIGHT
            + Fore.CYAN
            + "Nissar Chababy (Funilrys) "
            + Style.RESET_ALL
            + "with the help of "
            + Style.BRIGHT
            + Fore.GREEN
            + "https://git.io/vND4m "
            + Style.RESET_ALL
            + "&& "
            + Style.BRIGHT
            + Fore.GREEN
            + "https://git.io/vND4a",
        ),
        add_help=False,
    )

    CURRENT_VALUE_FORMAT = Fore.YELLOW + Style.BRIGHT + "Installed value: " + Fore.BLUE

    PARSER.add_argument(
        "-ad",
        "--adblock",
        action="store_true",
        help="Switch the decoding of the adblock format. %s"
        % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["adblock"]) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "-a",
        "--all",
        action="store_false",
        help="Output all available informations on screen. %s"
        % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["less"]) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "--cmd-before-end",
        type=str,
        help="Pass a command before the results (final) commit of travis \
        mode. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["command_before_end"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument(
        "-c",
        "--auto-continue",
        "--continue",
        action="store_true",
        help="Switch the value of the auto continue mode. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["auto_continue"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument(
        "--autosave-minutes",
        type=int,
        help="Update the minimum of minutes before we start commiting \
            to upstream under Travis CI. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["travis_autosave_minutes"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument(
        "--clean", action="store_true", help="Clean all files under output."
    )
    PARSER.add_argument(
        "--commit-autosave-message",
        type=str,
        help="Replace the default autosave commit message. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["travis_autosave_commit"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument(
        "--commit-results-message",
        type=str,
        help="Replace the default results (final) commit message. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["travis_autosave_final_commit"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument("-d", "--domain", type=str, help="Analyze the given domain.")
    PARSER.add_argument(
        "-db",
        "--database",
        action="store_true",
        help="Switch the value of the usage of a database to store \
            inactive domains of the currently tested list. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["inactive_database"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument(
        "-dbr",
        "--days-between-db-retest",
        type=int,
        help="Set the numbers of day(s) between each retest of domains present \
        into inactive-db.json. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["days_between_db_retest"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument(
        "--debug",
        action="store_true",
        help="Switch the value of the debug mode. %s"
        % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["debug"]) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "--dev",
        action="store_false",
        help="Activate the download of the developement version of PyFunceble.",
    )
    PARSER.add_argument(
        "--directory-structure",
        action="store_true",
        help="Generate the directory and files that are needed and which does \
            not exist in the current directory.",
    )
    PARSER.add_argument(
        "-f", "--file", type=str, help="Test a file with a list of domains."
    )
    PARSER.add_argument("--filter", type=str, help="Domain to filter.")
    PARSER.add_argument(
        "-ex",
        "--execution",
        action="store_true",
        help="Switch the dafault value of the execution time showing. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["show_execution_time"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument(
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit.",
    )
    PARSER.add_argument(
        "-h",
        "--host",
        action="store_true",
        help="Switch the value of the generation of hosts file. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["generate_hosts"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument(
        "--http",
        action="store_true",
        help="Switch the value of the usage of HTTP code. %s"
        % (CURRENT_VALUE_FORMAT + repr(HTTP_CODE["active"]) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "--iana", action="store_true", help="Update `iana-domains-db.json`."
    )
    PARSER.add_argument(
        "-ip",
        type=str,
        help="Change the ip to print in host file. %s"
        % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["custom_ip"]) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "--less",
        action="store_true",
        help="Output less informations on screen. %s"
        % (CURRENT_VALUE_FORMAT + repr(PyFunceble.switch("less")) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "-n",
        "--no-files",
        action="store_true",
        help="Switch the value the production of output files. %s"
        % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["no_files"]) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "-nl",
        "--no-logs",
        action="store_true",
        help="Switch the value of the production of logs files in case we \
        encounter some errors. %s"
        % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["logs"]) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "-nu",
        "--no-unified",
        action="store_true",
        help="Switch the value of the production of result.txt as unified result \
            under the output directory. %s"
        % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["unified"]) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "-nw",
        "--no-whois",
        action="store_true",
        help="Switch the value the usage of whois to test domain's status. %s"
        % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["no_whois"]) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "-p",
        "--percentage",
        action="store_true",
        help="Switch the value of the percentage output mode. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["show_percentage"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument(
        "--plain",
        action="store_true",
        help="Switch the value of the generation \
            of the plain list of domain. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["plain_list_domain"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument(
        "--production",
        action="store_true",
        help="Prepare the repository for production.",
    )
    PARSER.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Run the script in quiet mode. %s"
        % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["quiet"]) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "--share-logs",
        action="store_true",
        help="Activate the sharing of logs to an API which helps manage logs in \
            order to make PyFunceble a better script. %s"
        % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["share_logs"]) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "-s",
        "--simple",
        action="store_true",
        help="Switch the value of the simple output mode. %s"
        % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["simple"]) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "--split",
        action="store_true",
        help="Switch the valur of the split of the generated output files. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["inactive_database"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument(
        "--stable",
        action="store_true",
        help="Activate the download of the stable version of PyFunceble.",
    )
    PARSER.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=3,
        help="Switch the value of the timeout. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["seconds_before_http_timeout"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument(
        "--travis",
        action="store_true",
        help="Activate the travis mode. %s"
        % (CURRENT_VALUE_FORMAT + repr(CONFIGURATION["travis"]) + Style.RESET_ALL),
    )
    PARSER.add_argument(
        "--travis-branch",
        type=str,
        default="master",
        help="Switch the branch name where we are going to push. %s"
        % (
            CURRENT_VALUE_FORMAT
            + repr(CONFIGURATION["travis_branch"])
            + Style.RESET_ALL
        ),
    )
    PARSER.add_argument(
        "-u",
        "--update",
        action="store_true",
        help=" Get the latest version of PyFunceble.",
    )
    PARSER.add_argument(
        "-v", "--version", action="version", version="%(prog)s 0.61.1-beta"
    )

    ARGS = PARSER.parse_args()

    if ARGS.less:
        CONFIGURATION.update({"less": ARGS.less})

    if ARGS.adblock:
        CONFIGURATION.update({"adblock": PyFunceble.switch("adblock")})

    if ARGS.auto_continue:
        CONFIGURATION.update({"auto_continue": PyFunceble.switch("auto_continue")})

    if ARGS.autosave_minutes:
        CONFIGURATION.update({"travis_autosave_minutes": ARGS.autosave_minutes})

    if ARGS.clean:
        PyFunceble.Clean(None)

    if ARGS.cmd_before_end:
        CONFIGURATION.update({"command_before_end": ARGS.cmd_before_end})

    if ARGS.commit_autosave_message:
        CONFIGURATION.update({"travis_autosave_commit": ARGS.commit_autosave_message})

    if ARGS.commit_results_message:
        CONFIGURATION.update(
            {"travis_autosave_final_commit": ARGS.commit_results_message}
        )

    if ARGS.database:
        CONFIGURATION.update(
            {"inactive_database": PyFunceble.switch("inactive_database")}
        )

    if ARGS.days_between_db_retest:
        CONFIGURATION.update({"days_between_db_retest": ARGS.days_between_db_retest})

    if ARGS.debug:
        CONFIGURATION.update({"debug": PyFunceble.switch("debug")})

    if ARGS.dev:
        CONFIGURATION.update({"stable": ARGS.dev})

    if ARGS.directory_structure:
        DirectoryStructure()

    if ARGS.execution:
        CONFIGURATION.update(
            {"show_execution_time": PyFunceble.switch("show_execution_time")}
        )

    if ARGS.filter:
        CONFIGURATION.update({"to_filter": ARGS.filter})

    if ARGS.host:
        CONFIGURATION.update({"generate_hosts": PyFunceble.switch("generate_hosts")})

    if ARGS.http:
        CONFIGURATION.update(
            {"http_code_status": PyFunceble.switch("http_code_status")}
        )

    if ARGS.iana:
        IANA()

    if ARGS.ip:
        CONFIGURATION.update({"custom_ip": ARGS.ip})

    if ARGS.no_files:
        CONFIGURATION.update({"no_files": PyFunceble.switch("no_files")})

    if ARGS.no_logs:
        CONFIGURATION.update({"logs": PyFunceble.switch("logs")})

    if ARGS.no_unified:
        CONFIGURATION.update({"unified": PyFunceble.switch("unified")})

    if ARGS.no_whois:
        CONFIGURATION.update({"no_whois": PyFunceble.switch("no_whois")})

    if ARGS.percentage:
        CONFIGURATION.update({"show_percentage": PyFunceble.switch("show_percentage")})

    if ARGS.plain:
        CONFIGURATION.update(
            {"plain_list_domain": PyFunceble.switch("plain_list_domain")}
        )

    if ARGS.production:
        DirectoryStructure(production=True)

    if ARGS.quiet:
        CONFIGURATION.update({"quiet": PyFunceble.switch("quiet")})

    if ARGS.share_logs:
        CONFIGURATION.update({"share_logs": PyFunceble.switch("share_logs")})

    if ARGS.simple:
        CONFIGURATION.update(
            {"simple": PyFunceble.switch("simple"), "quiet": PyFunceble.switch("quiet")}
        )

    if ARGS.split:
        CONFIGURATION.update({"split": PyFunceble.switch("split")})

    if ARGS.stable:
        CONFIGURATION.update({"stable": ARGS.stable})

    if ARGS.timeout:
        if ARGS.timeout % 3 == 0:
            CONFIGURATION.update({"seconds_before_http_timeout": ARGS.timeout})

    if ARGS.travis:
        CONFIGURATION.update({"travis": PyFunceble.switch("travis")})

    if ARGS.travis_branch:
        CONFIGURATION.update({"travis_branch": ARGS.travis_branch})

    if ARGS.update:
        Update()

    if not CONFIGURATION["quiet"]:
        print(Fore.YELLOW + PYFUNCEBLE_LOGO)
    PyFunceble(ARGS.domain, ARGS.file)
