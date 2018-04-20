I'm really glad you're reading this, because we need contributions to make this tool one of the best tool around the Internet!

# Submitting changes

Before anything, please keep in mind the following. If one or more of those conditions are not filled. Your Pull Request to PyFunceble will not be merged.

The `master` branch is used only for releasing a new version of the code that's why we require that all contributions/modifications must be done under the `dev` or a new branch.

In order to gain sometime and also understand what you are working on, your pull requests submission as long as your commit descriptions should be clear and complete as much as possible. We do an exception for commit with minor changed but big changes should have a complete description. Please ensure to use the following method when commiting a big change.

```
$ ./tool.py -p && git commit -S -m "A summary of the commit" -m "A paragraph
> or a sentence explaining what changed, why and its impact."
```

All your commits should be signed with **PGP** _(Please read more [here](https://github.com/blog/2144-gpg-signature-verification))_.

Please note the usage of `-S` into the commit command which means that we sign the commit. The usage of `./tool.py -p` ensure that you don't break the code for everyone.

# Coding conventions

- We indend using tabs.
- We make sure that a method, a function and a class has a doctring.
- One line should not exceed 100 characters. But there is an exception for regular expressions.
- We follow at least PEP8.
- Our code should pass `pylint *.py` with at least a score of 9.95/10.
- Do not forget to run `./tool.py -p` before any commits.
