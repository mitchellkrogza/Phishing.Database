- [Phishing domain(s)](#phishing-domains)
- [Q\&A](#qa)
- [False Positives](#false-positives)
    - [Please do also notify](#please-do-also-notify)
- [Create a Pull Request for faster handling](#create-a-pull-request-for-faster-handling)
- [Bug reporting](#bug-reporting)
- [Open Source Project domain reporting tools](#open-source-project-domain-reporting-tools)
- [Document revision](#document-revision)

## Phishing domain(s)
If you would like to report a single or a bunch of phishing, there are a
coupe of options, but none of them goes into this repository.

Therefore, we recommanding you to report to ffollwing projects:

Amung the most solid and reliable projects you can report to is:

1. [Mitchell Krogza Phishing + Whitelist][MP], All manual labour
2. You can option for one of [My Privacy DNS][MYPDNSTL] many
   automatisation and bulk commit tools.
3. Phistank
4. OpenPhish

## Q&A

Q: Why are you recommending these projects over others?

A: Well Let's be honest, @spirillen are amung the moderators on both MK's
**Phishing** and **My Privacy DNS** projects and probably the most active and
online avatar on both blacklists.  
While both @funilrys and @mitchellkrogza are all Github and less online.

If you ask me (@spirillen) I would go for [My privacy DNS][MYPDNS] when
it comes for reporting any item to be blacklisted, while for whitelisting
(Not FalsePositives) your should 100% go for
[Mitchell Krogza Phishing + Whitelist][MP].

For reporting falsepositive you should absolutely ensure all (mentioned
above) and invloved projects get informed.

## False Positives

We understand being listed on a Phishing Database like this can be frustrating
and embarrassing for many web site owners. The first step is to remain calm.
The second step is to rest assured one of our maintainers will address your
issue as soon as possible.

Please make sure you have provided as much information as possible to help
speed up the process.

#### Please do also notify

You should please also inform [My Privacy DNS][MYPDNS], you can search for
the url/domain at <https://mypdns.eu.org/matrix/is_listed/>

## Create a Pull Request for faster handling

Users who understand git can creat a Pull Requests, an assist us for faster
removals by sending a PR to the manual repository of 
[Mitchell Krogza Phishing + Whitelist][MP] repository and add the FP domain
one of the whitelists:

  - [falsepositive.list][MPFL] matches `1 on 1`
  - [falsepositive_regex.list][MPFLRGX] matches against regex.
  - [falsepositive_rzd.list][MPFLRZD] This list will tell the system to 
    explicitly check for the given string plus all possible TLD.

Please include the same information as above to help speed up the whitelisting
process.

You should note that you should not expect merges are done in
[Mitchell Krogza Phishing + Whitelist][MP] until the issue have been solved
here, this is because those who can merge do not have access to the logs for
why your domain got listed.

## Bug reporting
When you are commiting bug reports please be as precise as possible and narrow
down the issue as much as you possible can.

If you have any questions recarding one of the MK's phishing or phishing DB
projects, please either just ask in the Bug report issue template and change
the title to `[Question]`

## Open Source Project domain reporting tools
Our friends over at [My Privacy DNS][MYPDNS] have a number of option for
you to easily and quickly add new domains to a number of categorised
blacklists including phishing.

1. By using the web, support anonymously reporting: [My Privacy DNS Webreporter][MyPDNSR]    
2. By installing one of the cool [Firefox add-ons, API, GUI, CLI tools][MYPDNSFF]
3. All of their [commit tools][MYPDNSTL]

[MP]: https://github.com/mitchellkrogza/phishing "Mitchell Krogza Phishing + Whitelist"
[MPFL]: https://github.com/mitchellkrogza/phishing/blob/main/falsepositive.list
[MPFLRGX]: https://github.com/mitchellkrogza/phishing/blob/main/falsepositive_regex.list
[MPFLRZD]: https://github.com/mitchellkrogza/phishing/blob/main/falsepositive_rzd.list
[MYPDNS]: https://mypdns.eu.org/ "My Privacy DNS Let no one spy on you online"
[MyPDNSR]: https://mypdns.eu.org/matrix/reporter/ "My Privacy DNS Webreporter"
[MYPDNSFF]: https://0xacab.org/my-privacy-dns/matrix/-/blob/master/tools/client_addon.md "My Privacy DNS Firefox Add-ons for easy domain reporting"
[MYPDNSTL]: https://0xacab.org/my-privacy-dns/matrix/-/blob/master/tools/README.md "My Privacy DNS easy issue commiting tools"

## Document revision

This is revision 0.1b

Last updated by @spirillen changed 1st of June 2023
