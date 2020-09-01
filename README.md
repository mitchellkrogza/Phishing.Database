<img src="https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/phishing-logo.jpg" alt="Phishing Domain Status Testing Repo"/>

# Phishing Domain Database <a href='https://twitter.com/PhishFindR'><img src="https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/twitter-35.png"/><img src="https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/spacer.jpg"/><img src="https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/spacer.jpg"/><img src='https://img.shields.io/twitter/follow/PhishFindR.svg?style=social&label=Follow' alt='Follow @PhishFindr'></a>

## NOTICE: Do Not Clone the repository and rely on Pulling the latest info !!! 
**This WILL BREAK daily** due to a complete reset of the repository history every 24 hours.
Please rely **ONLY** on pulling individual list files or the full list of [domains in tar.gz format](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/ALL-phishing-domains.tar.gz) and [links in tar.gz format](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/ALL-phishing-links.tar.gz) (updated hourly) using wget or curl.

_______________
#### Version: 21915 (2020-09-01 23:16:07 SAST)
| :boom: Latest Threats<br/>@ 23:16:07 | :boom: Active Threats<br/>Tuesday 2020-09-01 | Total Links<br/>Discovered Today |
| :---: | :---: |:---: |
| :warning: [1](https://github.com/mitchellkrogza/Phishing.Database/blob/master/phishing-links-ACTIVE-NOW.txt) | :warning: [2816](https://github.com/mitchellkrogza/Phishing.Database/blob/master/phishing-links-ACTIVE-TODAY.txt) | [3066](https://github.com/mitchellkrogza/Phishing.Database/blob/master/phishing-links-NEW-today.txt) |
*****************************
| Phishing Domains Status  | Domain Count | Percentage | Last Tested | Download |
| ---: | :---: | :---: | :---: |:---: |
| ACTIVE <img src=https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/green.jpg/> | [71328](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-ACTIVE.txt)  | 36 % | 2020-04-10 12:42:26 +0200 | [Download](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-ACTIVE.txt) |
| INACTIVE <img src=https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/red.jpg/>  | [27690](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-INACTIVE.txt)  | 14 % | 2020-04-10 12:42:26 +0200 | [Download](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-INACTIVE.txt) |
| INVALID <img src=https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/blue.jpg/> | [197](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-INVALID.txt)  | 0 % | 2020-04-10 12:42:26 +0200 | [Download](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-INVALID.txt) |
*****************************
| &emsp;&ensp;Phishing Links Status | &emsp;Link Count &ensp; | Percentage | Last Tested | Download |
| ---: | :---: | :---: | :---: |:---: |
| ACTIVE <img src=https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/green.jpg/> | [37577](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-ACTIVE.txt)  | 7 % | 2019-10-21 09:17:55 +0200 | [Download](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-ACTIVE.txt) |
| INACTIVE <img src=https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/red.jpg/>  | [40834](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-INACTIVE.txt)  | 8 % | 2019-10-21 09:17:55 +0200 | [Download](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-INACTIVE.txt) |
| INVALID <img src=https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/blue.jpg/> | [68](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-INVALID.txt)  | 0 % | 2019-10-21 09:17:55 +0200 | [Download](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-INVALID.txt) |
*****************************
#### Total Phishing Domains Captured: [197578](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/ALL-phishing-domains.tar.gz) << (FILE SIZE: 1.6M tar.gz)
#### Total Phishing Links Captured: [507252](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/ALL-phishing-links.tar.gz) << (FILE SIZE: 11M tar.gz)
____________________


## Purpose of this repo?

A Testing Repository for Phishing Domains, Web Sites and Threats. Above are results of Domains that have been tested to be Active, Inactive or Invalid. These Lists update hourly. This is just one of a number of extensive projects dealing with testing the status of harmful domain names and web sites. We test sources of Phishing attacks to keep track of how many of the domain names used in Phishing attacks are still active and functioning. We sort all domains from all sources into one list, removing any duplicates so that we have a clean list of domains to work with.

## Additions

### Add Phishing Domains
To add domains to this database send a Pull Request on the file https://github.com/mitchellkrogza/Phishing.Database/input-source/domains/public-domain-additions.txt
- include the domain name only (no http / https) eg. www.thisisphishing.com and not https://www.thisisphishing.com/

### Add Phishing Urls / Links
To add links / urls to this database send a Pull Request on the file https://github.com/mitchellkrogza/Phishing.Database/input-source/urls/public-url-additions.txt
- Include the full link

************************************************
## Define an Active Status

We define ACTIVE domains or links as any of the HTTP Status Codes Below. 
All the following HTTP status codes we regard as ACTIVE or still POTENTIALLY ACTIVE.

- ACTIVE HTTP Codes
```
- 100
- 101
- 200
- 201
- 202
- 203
- 204
- 205
- 206
```
- POTENTIALLY ACTIVE HTTP Codes
```
- 000
- 300
- 301
- 302
- 303
- 304
- 305
- 307
- 403
- 405
- 406
- 407
- 408
- 411
- 413
- 417
- 500
- 501
- 502
- 503
- 504
- 505
```
- POTENTIALLY INACTIVE HTTP Codes
```
- 400
- 402
- 403
- 404
- 409
- 410
- 412
- 414
- 415
- 416
```

Criminals planting Phishing links often resort to a variety of techniques like returning a variety of HTTP failure codes to trick people into thinking the link is gone but in reality if you test a bit later it is often back. 

Our System also tests and re-tests anything flagged as INACTIVE or INVALID.

************************************************
## How do you test?

We make use of the awesome [PyFunceble Testing Suite](https://github.com/funilrys/PyFunceble) written by [Nissar Chababy](https://github.com/funilrys/). Over 2 years in development this testing tool really provides us with a reliable source of active and inactive domains and through regular testing even domains which are inactive and may become active again are automatically moved back to the active list. [Read More about PyFunceble](https://pyfunceble.readthedocs.io/en/latest/)

************************************************
## Contributing

If you have a source list of phishing domains or links please consider contributing them to this project for testing? 
Simply send a PR adding your input source details and we will add the source. 

************************************************
## Please Remove my Domain From This List !!

If your domain was listed as being involved in Phishing due to your site being hacked or some other reason, please file a [False Positive report](https://github.com/mitchellkrogza/Phishing.Database/issues/new?assignees=mitchellkrogza%2C+funilrys&labels=false+positive&template=false-positive.md&title=%5BFALSE-POSITIVE%5D+) it unfortunately happens to many web site owners.

Make sure to include links in your report to where else your domain / web site was removed and whitelisted ie. Phishtank / Openphish or it might not be removed here at all.

************************************************
## Some Domains from Major reputable companies appear on these lists?

Lots of Phishing, Malware and Ransomware links are planted onto very reputable services. We automatically remove [Whitelisted Domains](https://github.com/Ultimate-Hosts-Blacklist/whitelist/blob/master/domains.list) from our list of published [Phishing Domains](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-domains-ACTIVE.txt). 

We do NOT however remove these and enforce an [Anti-Whitelist](https://github.com/mitchellkrogza/Phishing.Database/blob/master/dev-tools/anti-whitelist.txt) from our phishing links/urls lists as these lists help other spam and cybersecurity services to discover new threats and get them taken down. Please send a PR to the [Anti-Whitelist](https://github.com/mitchellkrogza/Phishing.Database/blob/master/dev-tools/anti-whitelist.txt) file to have something important re-included into the [Phishing Links](https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links-ACTIVE.txt) lists. The Anti-Whitelist only filters through link (url) lists and not domain lists.

************************************************
## Keep Threat Intelligence Free and Open Source

We are firm believers that threat intelligence on Phishing, Malware and Ransomware should always remain free and open source. Open disclosure of any criminal activity such as Phishing, Malware and Ransomware is not only vital to the protection of every internet user and corporation but also vital to the gathering of intelligence in order to shut down these criminal sites. Selling access to phishing data under the guises of "protection" is somewhat questionable. 


[<img src="https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/kofi5.png" alt="Buy me Coffee"/>](https://ko-fi.com/mitchellkrog)


************************************************
## Contributors

- [Mitchell Krog](https://github.com/mitchellkrogza/) [<img src="https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/kofi5.png" alt="Buy me Coffee" width="75"/>](https://ko-fi.com/mitchellkrog)
- [Nissar Chababy](https://github.com/funilrys/) [<img src="https://github.com/mitchellkrogza/Phishing.Database/blob/master/assets/kofi5.png" alt="Buy me Coffee" width="75"/>](https://ko-fi.com/funilrys)

************************************************
MIT License

Copyright (c) 2018 Mitchell Krog
https://github.com/mitchellkrogza

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
