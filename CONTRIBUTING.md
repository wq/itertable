# Contributing Guidelines

Thanks for contributing to IterTable!  Here are some guidelines to help you get started.

## Questions

Questions and ideas can be submitted to the [Django Data Wizard discussion board](https://github.com/wq/django-data-wizard/discussions).

## Bug Reports

Bug reports can be submitted to either [IterTable issues](https://github.com/wq/itertable/issues) or [Django Data Wizard issues](https://github.com/wq/itertable/issues).  Reports can take any form as long as there is enough information to diagnose the problem.  To speed up response time, try to include the following whenever possible:
 * Versions of Fiona and/or Pandas, if applicable
 * Expected (or ideal) behavior
 * Actual behavior

## Pull Requests

Pull requests are very welcome and will be reviewed and merged as time allows.  To speed up reviews, try to include the following whenever possible:
 * Reference the issue that the PR fixes (e.g. [#3](https://github.com/wq/itertable/issues/3))
 * Failing test case fixed by the PR
 * If the PR provides new functionality, update [the documentation](https://github.com/wq/django-data-wizard/tree/main/docs/itertable)
 * Ensure the PR passes lint and unit tests.  This happens automatically, but you can also run these locally with the following commands:
 
```bash 
python -m unittest discover -s tests -t . -v   # run the test suite
flake8 # run code style checking
```
