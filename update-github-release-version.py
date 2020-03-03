import os
import sys

from itertools import chain

from github import Github

import semver


if "GITHUB_TOKEN" not in os.environ:
    print("GITHUB_TOKEN environment variable not set!")
    sys.exit(1)


gh = Github(os.environ["GITHUB_TOKEN"])


def get_releases(repo):
    releases = list(repo.get_releases())
    # Draft release
    if not releases:
        print("No releases found!")
        sys.exit(1)

    # Always the first
    draft_release = releases[0]
    if not draft_release.draft:
        print("No draft release found!")
        sys.exit(1)

    for release in releases:
        if not release.draft:
            break
    else:
        print(f"Current release not found!")
        sys.exit(1)
    return draft_release, release


def update_release():
    repo = gh.get_repo(os.environ["GITHUB_REPOSITORY"])
    draft_release, release = get_releases(repo)

    current_version = semver.parse_version_info(release.title)
    commits = list(
        repo.get_commits(sha="development", since=release.published_at)
    )
    sha_commits = {commit.sha for commit in commits}
    # Expensive. We might revisit it in the future
    # https://developer.github.com/v3/repos/commits/#list-pull-requests-associated-with-commit  # noqa
    # https://github.com/PyGithub/PyGithub/issues/1414
    pulls = []
    gh_pulls = repo.get_pulls(state="closed", sort="updated", direction="desc")
    for pull in gh_pulls:
        # We need to iterate through all the pull requests because a PR
        # can be updated even after it's merged. *sigh*
        if not pull.merged_at or pull.merged_at < release.published_at:
            continue
        pull_sha_commits = {commit.sha for commit in pull.get_commits()}
        if pull_sha_commits & sha_commits:
            # This PR was merged and this code is on development branch
            pulls.append(pull)
    # Check for `major` and `minor` labels
    labels = chain(*[pull.labels for pull in pulls])
    labels = {l.name for l in labels}
    if "bump-major" in labels:
        next_version = str(current_version.bump_major())
    elif "bump-minor" in labels:
        next_version = str(current_version.bump_minor())
    else:
        next_version = str(current_version.bump_patch())
    # Update draft request with the new name
    draft_release.update_release(
        name=next_version, message=draft_release.body, draft=True
    )


if __name__ == "__main__":
    update_release()
