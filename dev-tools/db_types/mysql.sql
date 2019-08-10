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
-- This file is part of the PyFunceble project. It provide the MySQL database structure.
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

CREATE TABLE IF NOT EXISTS pyfunceble_auto_continue (
    id BIGINT(20) PRIMARY KEY AUTO_INCREMENT,
    file_path LONGTEXT NOT NULL,
    subject LONGTEXT NOT NULL,
    status VARCHAR(12) NOT NULL,
    is_complement TINYINT(1) NOT NULL,
    digest VARCHAR(64) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(digest)
);

DROP TRIGGER IF EXISTS updatePyFuncebleAutoContinueDates;
DELIMITER ///
CREATE TRIGGER updatePyFuncebleAutoContinueDates
    BEFORE UPDATE ON pyfunceble_auto_continue FOR EACH ROW
BEGIN
    IF NEW.modified <= OLD.modified THEN
        SET NEW.modified = CURRENT_TIMESTAMP;
    END IF;
END ///
DELIMITER ;

CREATE TABLE IF NOT EXISTS pyfunceble_inactive (
    id BIGINT(20) PRIMARY KEY AUTO_INCREMENT,
    file_path LONGTEXT NOT NULL,
    subject LONGTEXT NOT NULL,
    status VARCHAR(12) NOT NULL,
    digest VARCHAR(64) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(digest)
);

DROP TRIGGER IF EXISTS updatePyFuncebleInactiveDates;
DELIMITER ///
CREATE TRIGGER updatePyFuncebleInactiveDates
    BEFORE UPDATE ON pyfunceble_inactive FOR EACH ROW
BEGIN
    IF NEW.modified <= OLD.modified THEN
        SET NEW.modified = CURRENT_TIMESTAMP;
    END IF;
END ///
DELIMITER ;

CREATE TABLE IF NOT EXISTS pyfunceble_mining (
    id BIGINT(20) PRIMARY KEY AUTO_INCREMENT,
    file_path LONGTEXT NOT NULL,
    subject LONGTEXT NOT NULL,
    mined LONGTEXT NOT NULL,
    digest VARCHAR(64) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(digest)
);

DROP TRIGGER IF EXISTS updatePyFuncebleMiningDates;
DELIMITER ///
CREATE TRIGGER updatePyFuncebleMiningDates
    BEFORE UPDATE ON pyfunceble_mining FOR EACH ROW
BEGIN
    IF NEW.modified <= OLD.modified THEN
        SET NEW.modified = CURRENT_TIMESTAMP;
    END IF;
END ///
DELIMITER ;

CREATE TABLE IF NOT EXISTS pyfunceble_whois (
    id BIGINT(20) PRIMARY KEY AUTO_INCREMENT,
    subject LONGTEXT NOT NULL,
    expiration_date VARCHAR(12) NOT NULL,
    expiration_date_epoch INTEGER(11) NOT NULL,
    state VARCHAR(12) NOT NULL,
    record LONGTEXT NOT NULL,
    digest VARCHAR(64) NOT NULL,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(digest)
);

DROP TRIGGER IF EXISTS updatePyFuncebleWhoisDates;
DELIMITER ///
CREATE TRIGGER updatePyFuncebleWhoisDates
    BEFORE UPDATE ON pyfunceble_whois FOR EACH ROW
BEGIN
    IF NEW.modified <= OLD.modified THEN
        SET NEW.modified = CURRENT_TIMESTAMP;
    END IF;
END ///
DELIMITER ;

