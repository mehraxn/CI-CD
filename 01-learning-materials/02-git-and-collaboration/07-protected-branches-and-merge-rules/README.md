# Protected Branches and Merge Rules

## Why Protect the Default Branch

A protected branch is governed by server-side rules that restrict how its reference can change. The default branch often supplies release and deployment pipelines, so an unreviewed or force-pushed change can affect users quickly. Protection turns agreed collaboration and CI expectations into enforceable controls.

Settings differ among GitHub, GitLab, Bitbucket, and other platforms. GitHub also provides repository rulesets that can apply rules to groups of branches or tags. Learn the intent of each control and verify current platform documentation before enabling it.

## Core Controls

- **Prevent direct pushes:** Require changes to enter through a pull or merge request. Some trusted automation identities may need narrowly scoped exceptions.
- **Required pull requests:** Create a review and evidence boundary before the target branch moves.
- **Required reviews:** Require one or more approvals from eligible reviewers. Approval count should reflect risk and team size.
- **Required status checks:** Name automated checks that must report success for the proposed commit.
- **Up-to-date requirement:** Require the proposal to be tested with current target-branch changes. This improves integration evidence but can cause repeated updates in a busy repository.
- **Conversation resolution:** Require blocking review discussions to be addressed or explicitly resolved.
- **Linear history:** Permit only history forms that do not add merge commits, usually squash or rebase merges.
- **Force-push restriction:** Prevent replacement of published branch history.
- **Deletion protection:** Prevent accidental removal of an important branch.
- **Merge restrictions:** Limit who or which applications may update the branch.

A **merge queue** can update and test proposed changes against current target state in a controlled order. It reduces the race where several pull requests are independently green but conflict when merged close together.

## CODEOWNERS and Specialized Review

A `CODEOWNERS` file maps paths to responsible reviewers on platforms that support it. Combined with rules, changes to security, infrastructure, or workflow files can require review from people familiar with those areas. Ownership should be maintained; a stale mapping can block work or create false confidence.

Signed-commit requirements can verify commit signatures. They do not confirm that the signer reviewed the change or that the content is safe. Use them as one layer rather than a substitute for CI and review.

## Least Privilege and Bypass Risk

Repository roles, workflow tokens, deployment credentials, and bypass permissions should follow least privilege. Administrator bypass can be necessary for recovery, but routine bypass teaches teams that controls are optional. Bypasses should be limited, visible, and reviewed.

Automation accounts also deserve scrutiny. A workflow with broad write permission can bypass human restrictions if compromised. Pin and review third-party automation, restrict token permissions, and separate deployment authorization from general repository write access where practical.

## Recommended Beginner Policy

```text
main branch:
- Require pull requests
- Require at least one approval
- Require CI checks to pass
- Block force pushes
- Block deletion
- Require review conversations to be resolved
```

For this learning repository, the required CI checks should correspond to real stable workflow jobs. Do not require a check that never reports for the selected event, or every pull request may become impossible to merge. Add an up-to-date requirement or merge queue only after understanding its effect on wait time and workflow triggers.

## Balancing Safety and Speed

More controls are not always safer. Excessive approvals can become rubber stamps. Slow checks can create large queues. Rules that cannot handle an urgent recovery invite unsafe bypass. Start with meaningful controls, measure friction and failure, then improve the pipeline and rules together.

Protection does not eliminate all risk. An approved malicious change, a compromised reviewer, a flawed required test, or an overly privileged workflow can still cause harm. Backups, audit logs, artifact controls, deployment protections, monitoring, and recovery remain necessary.

## Project Connections

[TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) provides pull-request checks that could be required. [KubeOps CI](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml) does the same. TaskOps CD and KubeOps image release react to `main`, increasing the importance of controlling merges.

Branch-protection and ruleset settings are hosted-platform state and are not proven by repository files. This lesson does not claim that the recommended policy is currently enabled.

## Common Mistakes

- Requiring checks that are flaky or do not run for pull requests.
- Giving many users or automation identities bypass permission.
- Allowing direct production-triggering pushes without a deliberate reason.
- Requiring approvals but dismissing reviews as a formality.
- Protecting `main` while leaving release tags mutable.
- Enabling a linear-history rule without agreeing on a merge method.
- Assuming protection replaces secure workflows and recovery planning.

## Practical Exercise

Spend 15-20 minutes viewing, without changing, the branch-protection or ruleset options available for a practice repository. Compare them with the beginner policy and note which exact CI check names would be required. If you lack access, create a paper configuration instead. Do not alter this repository's settings.

## Knowledge Check

1. Why are required status checks useful?
2. What risk does blocking force pushes reduce?
3. Why can too many required approvals become ineffective?
4. What problem can a merge queue solve?
5. Do protected branches eliminate all repository risk?

<details>
<summary>View answers</summary>

1. They prevent merging a commit that lacks successful configured automated evidence.
2. Replacement or loss of published shared history.
3. Reviewers may approve mechanically, and delays may encourage bypass rather than thoughtful review.
4. It tests and merges proposals against the changing target in a controlled sequence.
5. No. Compromised identities, unsafe workflows, flawed checks, and approved harmful changes remain possible.

</details>

## Navigation

- [Back to Git and Collaboration](../README.md)
- [Previous: Tags, Versioning, and Releases](../06-tags-versioning-and-releases/)
- [Back to All Learning Materials](../../README.md)
