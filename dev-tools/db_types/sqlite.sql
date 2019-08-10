-- -- The tool to check the availability or syntax of domains, IPv4 or URL.
-- --
-- ::
--
--
--     ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
--     ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
--     ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
--     ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
--     ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
--     ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝
--
-- This file is part of the PyFunceble project. It provide the SQLite database structure.
--
-- Author:
--     Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom
--
-- Special thanks:
--     https://pyfunceble.github.io/special-thanks.html
--
-- Contributors:
--     https://pyfunceble.github.io/contributors.html
--
-- Project link:
--     https://github.com/funilrys/PyFunceble
--
-- Project documentation:
--     https://pyfunceble.readthedocs.io/en/dev/
--
-- Project homepage:
--     https://pyfunceble.github.io/
--
-- License:
-- ::
--
--
--     MIT License
--
--     Copyright (c) 2017, 2018, 2019 Nissar Chababy
--
--     Permission is hereby granted, free of charge, to any person obtaining a copy
--     of this software and associated documentation files (the "Software"), to deal
--     in the Software without restriction, including without limitation the rights
--     to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
--     copies of the Software, and to permit persons to whom the Software is
--     furnished to do so, subject to the following conditions:
--
--     The above copyright notice and this permission notice shall be included in all
--     copies or substantial portions of the Software.
--
--     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
--     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
--     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
--     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
--     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
--     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
--     SOFTWARE.

CREATE TABLE IF NOT EXISTS auto_continue (
    id INTEGER PRIMARY KEY,
    file_path TEXT NOT NULL,
    subject TEXT NOT NULL,
    status TEXT NOT NULL,
    is_complement INTEGER NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_path, subject)
);

CREATE TRIGGER IF NOT EXISTS updateAutoContinueDates
    AFTER UPDATE
    ON auto_continue
    FOR EACH ROW
    WHEN NEW.modified <= old.modified
BEGIN
    UPDATE auto_continue SET modified=CURRENT_TIMESTAMP WHERE id=OLD.id;
END;

CREATE TABLE IF NOT EXISTS inactive (
    id INTEGER PRIMARY KEY,
    file_path TEXT NOT NULL,
    subject TEXT NOT NULL,
    status INTEGER NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_path, subject)
);

CREATE TRIGGER IF NOT EXISTS updateInactiveDates
    AFTER UPDATE
    ON inactive
    FOR EACH ROW
    WHEN NEW.modified <= old.modified
BEGIN
    UPDATE inactive SET modified=CURRENT_TIMESTAMP WHERE id=OLD.id;
END;

CREATE TABLE IF NOT EXISTS mining (
    id INTEGER PRIMARY KEY,
    file_path TEXT NOT NULL,
    subject TEXT NOT NULL,
    mined TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(file_path, subject, mined)
);

CREATE TRIGGER IF NOT EXISTS updateMiningDates
    AFTER UPDATE
    ON mining
    FOR EACH ROW
    WHEN NEW.modified <= old.modified
BEGIN
    UPDATE mining SET modified=CURRENT_TIMESTAMP WHERE id=OLD.id;
END;

CREATE TABLE IF NOT EXISTS whois (
    id INTEGER PRIMARY KEY,
    subject TEXT NOT NULL,
    expiration_date TEXT NOT NULL,
    expiration_date_epoch INTEGER NOT NULL,
    state TEXT NOT NULL,
    record TEXT NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(subject)
);

CREATE TRIGGER IF NOT EXISTS updateWhoisDates
    AFTER UPDATE
    ON whois
    FOR EACH ROW
    WHEN NEW.modified <= old.modified
BEGIN
    UPDATE whois SET modified=CURRENT_TIMESTAMP WHERE id=OLD.id;
END;