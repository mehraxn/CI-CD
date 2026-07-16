# Branches, Merging, and Rebasing

## Branches and Parallel Work

A Git branch is a movable name that points to a commit. Creating a branch is inexpensive because Git does not copy every project file. The default branch, commonly `main`, represents the team's shared integration line. A feature branch gives a change a temporary name and review boundary.

Short-lived branches help continuous integration because they remain close to `main`. Long-lived branches collect assumptions and conflicts, delaying the moment when changes are tested together.

Basic commands:

```bash
git switch -c feature/add-health-check
git switch main
git merge feature/add-health-check
git rebase main
git branch -d feature/add-health-check
```

`git switch -c` creates and checks out a branch. `git switch main` changes the working tree to `main`. `git merge` integrates another branch into the current one. `git rebase main`, when run from the feature branch, replaces its unique commits on top of current `main`. `git branch -d` safely deletes a fully merged local branch.

## Local, Remote, and Upstream Branches

A local branch and a remote-tracking reference such as `origin/main` are separate names. Fetching updates the remote-tracking view. An **upstream** association tells commands such as `git pull` and `git push` which remote branch corresponds to the current local branch.

```bash
git push -u origin feature/add-health-check
git fetch origin
git branch -vv
```

The first command publishes the branch and records its upstream. Fetch updates remote information without integrating. `git branch -vv` shows tracking and divergence information.

## Merge Behavior

A **fast-forward merge** occurs when the target branch has no new divergent commits. Git can move the target branch pointer forward without creating a merge commit.

A **merge commit** combines two histories and has both tips as parents. It preserves the point at which branches came together.

Before merge:

```text
A---B---C main
     \
      D---E feature
```

After both lines have diverged, a merge commit can produce:

```text
A---B---C------M main
     \        /
      D------E
```

A **squash merge** applies the combined feature changes as one new commit on the target. It produces a compact default-branch history but does not preserve the feature commits as ancestors of the new commit. The original branch should then be considered merged through its content, not through a normal merge relationship.

## Rebase

Rebase takes commits unique to the current branch and replays their changes onto a new base. From the feature branch, `git rebase main` can produce:

```text
A---B---C---D'---E' feature
```

`D'` and `E'` contain corresponding changes but are new commits with new identities and parents. Rebasing rewrites commit identities. It is useful for updating a private feature branch and producing a linear sequence before review, but rebasing a shared branch forces collaborators to reconcile replaced history.

Interactive rebase, started with a command such as `git rebase -i HEAD~3`, can reorder, combine, edit, or drop local commits. It is powerful cleanup for unpublished work. Review the resulting diff and rerun checks because the rewritten commits are new.

## Merge or Rebase?

Merge preserves existing identities and the topology of collaboration. Rebase creates a linear presentation but rewrites the rebased commits. Neither is universally superior.

- Merge a shared branch when preserving published history matters.
- Rebase a private feature branch when the team permits it and a current base simplifies review.
- Use squash merging consistently when the team wants one default-branch commit per pull request.
- Never rebase or force-update a shared protected branch casually.

## Merge Conflicts

A conflict occurs when Git cannot combine changes automatically, often because both sides changed the same lines or one side deleted a file the other changed. Git marks unresolved paths in `git status` and may add conflict markers to text files.

Resolve a conflict by understanding both intended changes, editing the file to the correct combined result, removing markers, testing, staging the resolution, and continuing the merge or rebase. During a merge use `git merge --abort` to return to the pre-merge state when necessary. During a rebase use `git rebase --continue` after each resolution or `git rebase --abort` to stop.

Do not choose "ours" or "theirs" merely to make the markers disappear. The combined behavior must be correct.

## Force-Push Risk

After a published feature branch is rebased, its remote reference cannot be updated with a normal fast-forward push. If rewriting that branch is agreed, `git push --force-with-lease` is safer than `--force` because it refuses to overwrite unexpected remote work. It is still a history rewrite and should not be used on shared or protected branches without explicit coordination.

## Branches and CI

Push and pull-request events can run branch-specific checks. A pull-request workflow may test the proposed merge context, while a push workflow validates the branch commit. Short-lived branches receive integration feedback sooner and reduce the gap between branch and default-branch results.

[TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) runs on pull requests and `main` pushes. Its CD workflow runs only after a push to `main`. This makes branch integration behavior directly relevant to deployment eligibility.

## Practical Exercise

In a disposable repository, create `main` and a temporary feature branch. Make different edits, merge the feature, and inspect the graph. Then create a second practice branch and rebase it onto a new `main` commit. Safety note: keep this local; do not force-push shared branches.

## Knowledge Check

1. What does a branch point to?
2. How does a merge commit differ from a rebase?
3. Why do rebased commits have new identities?
4. Why is `--force-with-lease` safer than `--force`?
5. Why do short-lived branches support CI?

<details>
<summary>View answers</summary>

1. A commit; the name moves when new commits are added to the branch.
2. A merge joins existing histories; rebase replaces commits on a new parent line.
3. Their parent metadata changes, so Git creates new commit objects.
4. It checks that the remote still matches the last known state before overwriting it.
5. They reduce divergence and expose integration problems earlier.

</details>

## Navigation

- [Back to Git and Collaboration](../README.md)
- [Previous: Commits and History](../02-commits-and-history/)
- [Next: Pull Requests and Code Review](../04-pull-requests-and-code-review/)
- [Back to All Learning Materials](../../README.md)
