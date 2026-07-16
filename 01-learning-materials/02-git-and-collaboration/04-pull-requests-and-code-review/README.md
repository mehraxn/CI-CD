# Pull Requests and Code Review

## What a Pull Request Is

A pull request proposes integrating changes from one branch into another. GitLab and some other platforms use the term **merge request**. The platform presents the difference, discussion, automated checks, approvals, and merge controls around an underlying Git branch relationship.

Teams use pull requests to review changes before shared history moves. They create a place to explain intent, discover defects, share knowledge, evaluate risk, and record decisions. A pull request is not a Git object stored inside commit history; it is collaboration data managed by a hosting platform.

## Branches, Events, and CI

An author pushes a branch and opens a pull request toward a target such as `main`. The platform can emit a pull-request event that starts CI. New commits normally update the proposal and rerun relevant checks. A **status check** reports a result associated with a commit. Repository rules may require named checks before merge.

CI helps reviewers by checking repeatable facts: tests, formatting, builds, scans, and policies. It does not replace thoughtful review of design, correctness, readability, operational consequences, or whether the change solves the intended problem.

## Preparing a Reviewable Pull Request

Small pull requests are easier to understand, test, and review. Separate unrelated cleanup from behavior changes. If a change must be large, explain its structure and suggest a review order.

A useful description gives context rather than repeating the diff:

```markdown
## Summary

Explain what changed and why.

## Changes

- Change one
- Change two

## Testing

Explain how the change was tested.

## Risks

Describe possible risks or side effects.

## Checklist

- [ ] Tests pass
- [ ] Documentation is updated
- [ ] No secrets were committed
```

Linking an issue can provide requirements and close tracking work according to platform conventions. The pull request should still be understandable without forcing reviewers to reconstruct its purpose from several links.

A **draft pull request** signals that work is not ready to merge while allowing early feedback and CI execution. Drafts are useful for uncertain design, but they should not become permanently stale substitutes for direct collaboration.

## Author Responsibilities

The author should self-review the diff, remove accidental files, provide evidence, call out risky decisions, respond to comments, and keep the branch reasonably current. A response can accept a suggestion, clarify reasoning, or propose an alternative. Silence or mechanical resolution of comments weakens shared understanding.

After changes, the author should confirm checks cover the new commit. If a branch was rebased or force-updated, previous approvals may no longer apply depending on repository rules.

## Reviewer Responsibilities

A reviewer should understand the goal, examine important behavior and failure paths, verify that tests match risks, and give constructive, specific feedback. Distinguish blocking problems from suggestions. Explain why a concern matters and ask questions when intent is unclear.

Synchronous review - pairing or a short call - helps when written comments become slow or contentious. Asynchronous review provides flexibility and a durable record. Effective teams use both rather than treating one as universally correct.

## Review Outcomes and Merge Methods

Reviewers may comment, approve, or request changes. Requested changes should describe what must be addressed before merge. Conversations should be resolved only after the concern is handled or a clear decision is recorded.

Merge conflicts arise when the source and target cannot be combined automatically. The author generally resolves them because the author knows the intended change, but reviewers should recheck affected behavior.

Common merge methods are:

- **Merge commit:** Preserves branch commits and records the join.
- **Squash merge:** Creates one target-branch commit containing the proposal's combined change.
- **Rebase merge:** Replays commits onto the target for a linear history.

Choose a method consistently so history remains predictable. After a successful merge, delete the feature branch when it is no longer needed; the merged commits remain in history.

## Common Review Mistakes

- Submitting large, unrelated changes without guidance.
- Reviewing style manually when a formatter can provide consistent feedback.
- Approving because CI is green without reading the change.
- Blocking on personal preference without an agreed standard.
- Giving vague comments such as "bad" or "fix this."
- Ignoring deployment, migration, security, or rollback implications.
- Letting requests remain open until their base and evidence are stale.
- Treating review as a contest between author and reviewer.

## Existing Project Connections

[TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) has a `pull_request` trigger and runs quality, test, security, image, and smoke-test work. [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) also validates pull requests. Repository files do not reveal current hosted approval or required-check settings, so those should be inspected in the platform rather than assumed.

## Practical Exercise

Prepare a draft pull-request description for a small documentation improvement using the template above. If you have a safe practice repository, open it as a draft and inspect triggered checks; otherwise keep the exercise local. Do not change settings or merge into this repository as part of the lesson.

## Knowledge Check

1. Why are small pull requests usually easier to review?
2. What can CI checks contribute, and what can they not replace?
3. When might synchronous review be preferable?
4. Why should the merge method be selected consistently?

<details>
<summary>View answers</summary>

1. They reduce context, risk, and the number of interacting changes.
2. CI supplies repeatable automated evidence but cannot replace human evaluation of intent, design, and broader consequences.
3. When design is uncertain or written discussion is slow, ambiguous, or contentious.
4. Predictable history makes later inspection, reverts, and release reasoning easier.

</details>

## Navigation

- [Back to Git and Collaboration](../README.md)
- [Previous: Branches, Merging, and Rebasing](../03-branches-merging-and-rebasing/)
- [Next: Branching Strategies](../05-branching-strategies/)
- [Back to All Learning Materials](../../README.md)
