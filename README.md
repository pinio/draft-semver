# draft-semver
Set a semantic-version number (patch/minor/major) on the current draft release

## Usage

This action requires you to have a draft release already. For this you can use other
actions, such as [Release Drafter](https://github.com/release-drafter/release-drafter),
calling draft-semver after to rename your draft release according to soome specified rules.

Draft-semver requires you to already have at least one non-draft release using semantic
version (for example, `1.0.0`). It theoretically searches for all pull requests with the
`bump-minor` or `bump-major` labels and defines the next version number according to
the existence of those labels. It will always go on the order major -> minor -> patch.

Example: Consider the current version as being `1.2.3`. If at least one PR has the
`bump-major` label, it will increase the major version of the draft release (on this
example, `2.0.0`). Otherwise, if at least one PR has the `bump-minor` label, it will
increase the minor version of the draft release (on this example, `1.3.0`). Otherwise,
it will just increase the patch version (on this example, `1.2.4`).

You should have the action on your action. One example, combining the usage with
Release Drafter:

```yaml
name: Create/update draft release

on:
  push:
    branches:
      - master

jobs:
  update_draft_release:
    runs-on: ubuntu-latest
    steps:
      - uses: release-drafter/release-drafter@v5
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - uses: pinio/draft-semver@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
