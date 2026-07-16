# Commits and History

## Commits as Connected Snapshots

A commit records a snapshot of the tracked project content, metadata such as author and time, a message, and one or more parent commits. Git identifies the commit with a hash derived from its contents and related metadata. A short hash is convenient for display; the full identifier is the stronger reference.

Commits form history through parent relationships. Most commits have one parent. A merge commit has multiple parents. Because changing an old commit creates a different hash, rewriting history also changes the identity of its descendants.

The **author** identifies who originally wrote the change. The **committer** identifies who recorded that version of the commit. They can differ after applying a patch, rebasing, or merging through a platform.

## Small, Focused, Atomic Commits

An atomic commit makes one coherent change and leaves the project in a reasonable state. It should not mix an unrelated refactor, a feature, generated files, and formatting across the project. Focused commits are easier to review, revert, cherry-pick, bisect, and associate with pipeline failures.

"Small" is about conceptual scope, not an exact line count. A schema change and its required application update may belong together because separating them would break the build.

## Commit Messages

A useful subject describes the outcome in an imperative style and enough context to distinguish it from other work. A longer body can explain why, tradeoffs, or migration notes.

Weak messages:

```text
fix
update
changes
```

Better messages:

```text
fix(api): reject invalid task identifiers
test(auth): add expired-token coverage
ci: run integration tests on pull requests
```

Conventional Commits is an optional convention using types such as `feat`, `fix`, `docs`, `test`, and `ci`, with an optional scope and breaking-change marker. It can support generated changelogs and version decisions, but teams must apply it consistently. A formatted prefix cannot rescue a vague description.

## Inspecting and Comparing History

Useful read-only commands include:

```bash
git log --oneline --decorate --graph --all
git show <commit>
git diff <older-commit>..<newer-commit>
git blame <file>
```

`git log` displays history; `git show` displays a commit and its patch; `git diff` compares two states. `git blame` associates lines with commits, but it should be used to find context, not blame a person.

## Correcting and Undoing Work

`git commit --amend` replaces the most recent commit with a new one containing corrected staged content or message. It is convenient before sharing. After a commit is shared, amending changes its identity and can disrupt collaborators.

Three commonly confused commands have different purposes:

- **`git revert <commit>`** creates a new commit that applies the inverse of an earlier change. It preserves shared history and is usually the safest way to undo an already shared commit.
- **`git reset`** moves a branch reference and can also change the staging area or working files depending on mode. It is useful for local correction but can discard work or rewrite shared history. Beginners should inspect status and understand `--soft`, default mixed, and `--hard` before use; `--hard` is destructive.
- **`git restore`** copies file content from the staging area or another source into the working directory, and with `--staged` can unstage. It works at the file-state level rather than creating a history record.

When a shared change must be undone, prefer `git revert`. Do not force-push casually to shared branches.

## Other History Tools

- **Cherry-pick:** Applies the change introduced by an existing commit as a new commit on the current branch. It is useful for targeted backports but duplicates change identity and can complicate later merges.
- **Bisect:** Uses binary search through history to find the first bad commit. It is especially effective when a repeatable automated test can label each candidate good or bad.
- **Signed commits:** Add cryptographic verification that a commit was signed by a particular key or identity mechanism. Verification helps establish origin but does not prove the code is correct or the signer was uncompromised.

## History and CI/CD

A pipeline run normally records a commit hash. Build artifacts and deployments should preserve that link. Focused history helps identify which change caused a failing pipeline and supports safe reverts. Rewriting a commit after results were recorded means the new commit has not passed those exact checks.

Avoid secrets in commits. Automated secret scanning can help, but prevention and review are still necessary. If a credential enters history, remove its access by revoking or rotating it immediately; deleting a visible line alone does not make the credential safe.

Project workflows use `${{ github.sha }}` to create traceable container tags. Inspect the [TaskOps CD workflow](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) and [KubeOps image release](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) for this commit-to-artifact connection.

## Practical Exercise

In a disposable practice repository, make two focused commits with meaningful messages. Use `git show` and `git diff` to compare them, then use `git revert` on the second commit and inspect the new history. Safety note: do not practice reset or force-push on shared branches.

## Knowledge Check

1. Why are focused commits useful when CI fails?
2. How do revert, reset, and restore differ?
3. Why does rebasing or amending change a commit hash?
4. What should happen if a secret is committed?

<details>
<summary>View answers</summary>

1. They reduce the possible cause and make the change easier to inspect or undo.
2. Revert adds an inverse commit; reset moves a reference and may alter local state; restore replaces file or staged content.
3. A commit identity depends on its content, metadata, and parent, so replacing any of those creates a new object.
4. Revoke or rotate it immediately, then follow the repository's incident and history-cleanup process.

</details>

## Navigation

- [Back to Git and Collaboration](../README.md)
- [Previous: Git Fundamentals](../01-git-fundamentals/)
- [Next: Branches, Merging, and Rebasing](../03-branches-merging-and-rebasing/)
- [Back to All Learning Materials](../../README.md)
