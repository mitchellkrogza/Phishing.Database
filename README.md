<img src="https://github.com/Phishing-Database/assets/raw/main/phishing-logo.jpg" alt="Phishing Domain Status Testing Repo"/>

# Phishing Domain Database <a href="https://twitter.com/PhishFindR" ><img src="https://img.shields.io/twitter/follow/PhishFindR.svg?style=social&label=Follow" /></a>


The **Phishing.Database** project is a comprehensive and regularly updated repository designed to help the community identify and mitigate phishing threats.

We believe that threat intelligence on phishing, malware, and ransomware should always remain **free and open-source**. By openly sharing data about criminal activities, we aim to protect the internet users, help organizations mitigate threats, and contribute to a safer online environment for everyone by contributing to the global effort to identify and shutdown malicious sites. Unlike proprietary systems that sell access to phishing data, we focus and on transparency and collaboration for the greater good.

Join us in our mission to keep threat intelligence free and open-source by contributing to the project, sharing the data, and supporting the maintainers.

---

|                                                                          **Repository**                                                                          |                                                                                                                                                              **Become a Sponsor**                                                                                                                                                              |
| :--------------------------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                           ![GitHub License](https://img.shields.io/github/license/mitchellkrogza/Phishing.Database?style=flat-square)                            | We're seeking sponsors to help us grow and strengthen our infrastructure. By sponsoring this project, you'll have the opportunity to showcase your logo and link here, gaining visibility and supporting an open-source initiative that benefits the community. <br> 📧 Contact us at contact@phish.co.za to explore partnership opportunities. |
| <a href='https://twitter.com/PhishFindR'><img src='https://img.shields.io/twitter/follow/PhishFindR.svg?style=social&label=Follow' alt='Follow @PhishFindR'></a> |                                                                                                                                Help keep this project's infrastructure thriving by supporting the maintainers!                                                                                                                                 |
|                                                                                                                                                                  |                                                                                         Support **@mitchellkrogza** on [Ko-fi](https://ko-fi.com/mitchellkrog)!<br>Sponsor **@funilrys** via [GitHub Sponsors](https://github.com/sponsors/funilrys)!                                                                                          |


---

#### Version: V.2024-12-17.05
|                                           :boom: Latest Threats<br/>@ 05:31:07                                            |                                        :boom: Active Threats<br/>Tuesday 2024-12-17                                         |                                             Total Links<br/>Discovered Today                                             |
| :---------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------: |
| :warning: [328779](https://github.com/mitchellkrogza/Phishing.Database/blob/master/phishing-links-ACTIVE-NOW.txt) | :warning: [1184](https://github.com/mitchellkrogza/Phishing.Database/blob/master/phishing-links-ACTIVE-today.txt) | [393](https://github.com/mitchellkrogza/Phishing.Database/blob/master/phishing-links-NEW-today.txt) |
*****************************
#### Total Phishing Domains Captured: [908](https://phish.co.za/latest/ALL-phishing-domains.tar.gz) << (FILE SIZE: 12K tar.gz)
#### Total Phishing Links Captured: [1376364](https://phish.co.za/latest/ALL-phishing-links.tar.gz) << (FILE SIZE: 28M tar.gz)

---

## DO NOT Clone The Repository

The repository undergoes a **history reset every 24 hours**, which will break your setup if you rely on cloning. breaking changes.

To ensure uninterrupted access to the data, please download the latest lists directly from the provided links below.

---

## File Sources

The links below will direct you to the latest data files for this project.

| File Name                     | Official Source                                                      |
| ----------------------------- | -------------------------------------------------------------------- |
| ALL-phishing-domains.lst      | [Download](https://phish.co.za/latest/ALL-phishing-domains.lst)      |
| ALL-phishing-links.lst        | [Download](https://phish.co.za/latest/ALL-phishing-links.lst)        |
| ALL-phishing-domains.tar.gz   | [Download](https://phish.co.za/latest/ALL-phishing-domains.tar.gz)   |
| ALL-phishing-links.tar.gz     | [Download](https://phish.co.za/latest/ALL-phishing-links.tar.gz)     |
| phishing-domains-ACTIVE.txt   | [Download](https://phish.co.za/latest/phishing-domains-ACTIVE.txt)   |
| phishing-domains-INACTIVE.txt | [Download](https://phish.co.za/latest/phishing-domains-INACTIVE.txt) |
| phishing-domains-INVALID.txt  | [Download](https://phish.co.za/latest/phishing-domains-INVALID.txt)  |
| phishing-IPs-ACTIVE.txt       | [Download](https://phish.co.za/latest/phishing-IPs-ACTIVE.txt)       |
| phishing-IPs-INACTIVE.txt     | [Download](https://phish.co.za/latest/phishing-IPs-INACTIVE.txt)     |
| phishing-IPs-INVALID.txt      | [Download](https://phish.co.za/latest/phishing-IPs-INVALID.txt)      |
| phishing-links-ACTIVE.txt     | [Download](https://phish.co.za/latest/phishing-links-ACTIVE.txt)     |
| phishing-links-INACTIVE.txt   | [Download](https://phish.co.za/latest/phishing-links-INACTIVE.txt)   |
| phishing-links-INVALID.txt    | [Download](https://phish.co.za/latest/phishing-links-INVALID.txt)    |


_The files are updated regularly._

---

## Automated Testing

The testing of the domains and URLs is automated using the awesome [PyFunceble Testing Suite](https://github.com/funilrys/PyFunceble) witten by Nissar Chababy _(AKA [@funilrys](https://github.com/funilrys))_. Over many years in development, this tool has become a robust and reliable source of domain and URL status. We use it in an automated environment which actively retests domains and URLs on a regular basis.

### Who do we define an active status?

We define an active status as a domain or URL that is currently active and serving phishing content.
The status is determined by the HTTP status code returned by the server.

#### Active Status Codes

- 100, 101, 200, 201, 202, 203, 204, 205, 206

#### Potentially Active Status Codes

- 000, 300, 301, 302, 303, 304, 305, 307, 403, 405, 406, 407, 408, 411, 413, 417, 500, 501, 502, 503, 504, 505

_Any of the status codes above are considered active until further investigation._

### Potentially Inactive Status Codes

- 400, 402, 403, 404, 409, 410, 412, 414, 415, 416

---
## Removal Requests

If your domain has been listed incorrectly due to hacking or other reasons, file a [False Positive Report](https://github.com/mitchellkrogza/Phishing.Database/issues/new/choose) with proof of removal from other platforms (e.g., Phishtank, Openphish) to expedite processing.

---

## Contributing

Contributions are welcome and encouraged.

### Data Contributions

To contribute, please submit follow the matrix below to identify the correct file and repository to submit your data.

| Action   | Data Type             | File to Edit                                                                                    |
| -------- | --------------------- | ----------------------------------------------------------------------------------------------- |
| ➕ Add    | Domain                | [add-domain](https://github.com/mitchellkrogza/phishing/blob/main/add-domain)                   |
| ➕ Add    | Domain (wildcard)     | [add-wildcard-domain](https://github.com/mitchellkrogza/phishing/blob/main/add-wildcard-domain) |
| ➕ Add    | Link                  | [add-link](https://github.com/mitchellkrogza/phishing/blob/main/add-link)                       |
| ➕ Add    | IP                    | [IP-addr.list](https://github.com/mitchellkrogza/phishing/blob/main/IP-addr.list)               |
| ➕ Add    | IP (cidr)             | [IP-addr.cidr.list](https://github.com/mitchellkrogza/phishing/blob/main/IP-addr.cidr.list)     |
| ❌ Remove | False Positive Domain | [falsepositive.list](https://github.com/mitchellkrogza/phishing/blob/main/falsepositive.list)   |

### Reporting Issues

To report an issue or a false positive, please submit a [new issue](https://github.com/mitchellkrogza/Phishing.Database/issues/new/choose).

---


## Authors

- Mitchell Krog ([@mitchellkrogza](https://github.com/mitchellkrogza)) - Support **@mitchellkrogza** on [Ko-fi](https://ko-fi.com/mitchellkrog)!

- Nissar Chababy ([@funilrys](https://github.com/funilrys)) - Sponsor **@funilrys** via [GitHub Sponsors](https://github.com/sponsors/funilrys)!

---

## License

```
MIT License

Copyright (c) 2018-2024 Mitchell Krog - @mitchellkrogza
Copyright (c) 2018-2024 Nissar Chababy - @funilrys

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