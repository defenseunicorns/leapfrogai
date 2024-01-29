# Contributing to LeapfrogAI (LFAI)

First off, thanks so much for wanting to help out! :tada:

This document describes the steps and requirements for contributing a bug fix or feature in a Pull Request to all LeapfrogAI products! If you have any questions about the process or the pull request you are working on feel free to reach out in the [LFAI Discord Channel](https://discord.gg/s2Ja5cmZRQ).

## Developer Experience

Continuous Delivery is core to our development philosophy. Check out [https://minimumcd.org](https://minimumcd.org/) for a good baseline agreement on what that means.

Specifically:

- We do trunk-based development (`main`) with short-lived feature branches that originate from the trunk, get merged into the trunk, and are deleted after the merge
- We don't merge code into `main` that isn't releasable
- We perform automated testing on all changes before they get merged to `main`
- We create ADRs for all architectural decisions
- Merges are always squashed and use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
- We create immutable release artifacts

### Developer Workflow

:key: == Required by automation

1. Look at the next due [issue] and pick an issue that you want to work on. If you don't see anything that interests you, create an issue and assign it to yourself.
2. Drop a comment in the issue to let everyone know you're working on it and submit a Draft PR (step 4) as soon as you are able. If you have any questions as you work through the code, reach out in the [LFAI Discord Channel](https://discord.gg/s2Ja5cmZRQ).
3. :key: Set up your Git config to GPG sign all commits. [Here's some documentation on how to set it up](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits). You won't be able to merge your PR if you have any unverified commits.
4. Create a Draft Pull Request as soon as you can, even if it is just 5 minutes after you started working on it. We lean towards working in the open as much as we can. If you're not sure what to put in the PR description, just put a link to the issue you're working on. If you're not sure what to put in the PR title, just put "WIP" (Work In Progress) and we'll help you out with the rest.
5. :key: Automated tests will begin based on the paths you have edited in your Pull Request.
   > ⚠️ **NOTE:** _If you are an external third-party contributor, the pipelines won't run until a [CODEOWNER](https://github.com/defenseunicorns/zarf/blob/main/CODEOWNERS) approves the pipeline run._
6. :key: Be sure to use the [needs-adr,needs-docs,needs-tests](https://github.com/defenseunicorns/zarf/labels?q=needs) labels as appropriate for the PR. Once you have addressed all of the needs, remove the label.
7. Once the review is complete and approved, a core member of the LeapfrogAI project will merge your PR. If you are an external third-party contributor, two core members of the zarf project will be required to approve the PR.
8. Close the issue if it is fully resolved by your PR. _Hint: You can add "Fixes #XX" to the PR description to automatically close an issue when the PR is merged._

## Testing

TBD

## Documentation

### Updating Our Documentation

Under construction.

### Architecture Decision Records (ADR)

We've chosen to use ADRs to document architecturally significant decisions. We primarily use the guidance found in [this article by Michael Nygard](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions) with a couple of tweaks:

- The criteria for when an ADR is needed is undefined. The team will decide when the team needs an ADR.
- We will use the tool [adr-tools](https://github.com/npryce/adr-tools) to make it easier on us to create and maintain ADRs.
- We will keep ADRs in the repository under `adr/NNNN-name-of-adr.md`. `adr-tools` is configured with a dotfile to automatically use this directory and format.

### How to use `adr-tools`

```bash
# Create a new ADR titled "Use Bisquick for all waffle making"
adr new Use Bisquick for all waffle making

# Create a new ADR that supersedes a previous one. Let's say, for example, that the previous ADR about Bisquick was ADR number 9.
adr new -s 9 Use scratch ingredients for all waffle making

# Create a new ADR that amends a previous one. Let's say the previous one was ADR number 15
adr new -l "15:Amends:Amended by" Use store-bought butter for all waffle making

# Get full help docs. There are all sorts of other helpful commands that help manage the decision log.
adr help
```
