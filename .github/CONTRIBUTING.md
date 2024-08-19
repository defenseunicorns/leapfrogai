# Welcome to LeapfrogAI

Thank you for your interest in LeapfrogAI!

This document describes the process and requirements for contributing.

## Developer Experience

Continuous Delivery is core to our development philosophy. Check out [https://minimumcd.org](https://minimumcd.org) for a good baseline agreement on what that means.

Specifically:

- We do trunk-based development (main) with short-lived feature branches that originate from the trunk, get merged into the trunk, and are deleted after the merge
- We don't merge code into main that isn't releasable
- We perform automated testing on all changes before they get merged to main
- Continuous integration (CI) pipeline tests are definitive
- We create immutable release artifacts

### Developer Workflow

:key: == Required by automation

1. Drop a comment in any issue to let everyone know you're working on it and submit a Draft PR (step 4) as soon as you are able.
2. :key: Set up your Git config to GPG sign all commits. [Here's some documentation on how to set it up](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits). You won't be able to merge your PR if you have any unverified commits.
3. Use the [pre-commit](https://pre-commit.com/) hooks to provide localized checks against your new or modified code to catch mistakes before pushing.

  - Pre-commit must be activated in a Python-enabled environment and installed to the local `.git` repository to activate the commit hooks properly
  - UDS and Zarf Lints require the [UDS tasks](../tasks.schema.json), [UDS](../uds.schema.json), and [Zarf](<(../zarf.schema.json)>) JSON schemas to be up-to-date with the current UDS CLI version (e.g., v0.14.0)

  ```bash
  wget https://raw.githubusercontent.com/defenseunicorns/uds-cli/v0.14.0/uds.schema.json
  wget https://raw.githubusercontent.com/defenseunicorns/uds-cli/v0.14.0/zarf.schema.json
  wget https://raw.githubusercontent.com/defenseunicorns/uds-cli/v0.14.0/tasks.schema.json
  ```

4. Create a Draft Pull Request as soon as you can, even if it is just 5 minutes after you started working on it. We lean towards working in the open as much as we can.

   > ⚠️ **NOTE:** _:key: We use [Conventional Commit messages](https://www.conventionalcommits.org/) in PR titles so, if you can, use one of `fix:`, `feat:`, `chore:`, `docs:` or similar. If you need help, just use with `wip:` and we'll help with the rest_

5. :key: Automated tests will begin based on the paths you have edited in your Pull Request.

   > ⚠️ **NOTE:** _If you are an external third-party contributor, the pipelines won't run until a [CODEOWNER](./CODEOWNERS) approves the pipeline run._

6. :key: Be sure to heed the `needs-adr`,`needs-docs`,`needs-tests` labels as appropriate for the PR. Once you have addressed all of the needs, remove the label or request a maintainer to remove it.
7. Once the review is complete and approved, a core member of the project will merge your PR. If you are an external third-party contributor, two core members (CODEOWNERS) of the project will be required to approve the PR.
8. Close the issue if it is fully resolved by your PR. _Hint: You can add "Fixes #XX" to the PR description to automatically close an issue when the PR is merged._

### Release Please

We've chosen Google's [release-please](https://github.com/googleapis/release-please#release-please) as our automated tag and release solution. Below are some basic usage instructions. Read the documentation provided in the link for more advanced usage.

- Use the conventional commits specification for all PRs that are merged into the `main` branch.
- To specify a specific version, like a patch or minor, you must provide an empty commit like this: `git commit --allow-empty -m "chore: release 0.1.0" -m "Release-As: 0.1.0"`
- Maintain and provide a `secrets.RELEASE_PLEASE_TOKEN` Personal Access Token (PAT) as identified in the GitHub workflow YAML.
