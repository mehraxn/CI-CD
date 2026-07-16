# Git Fundamentals

## Version Control and Git

Version control records changes to files over time so people can inspect history, compare states, collaborate, and recover earlier work. Git is a distributed version-control system. Each normal clone contains project files plus enough repository history for most work, so commits and history inspection do not require constant server access.

Distributed does not mean uncoordinated. Teams usually designate a hosted remote repository as the collaboration source and agree on a default branch, review process, and release references.

## The Repository State Model

- **Repository:** The tracked project history and references managed by Git.
- **Working directory:** The checked-out files that you view and edit.
- **Staging area:** The proposed contents of the next commit, also called the index.
- **Local repository:** Your local commits, branches, tags, and Git metadata.
- **Remote repository:** A repository reached over a network and used to exchange work.
- **Commit:** A snapshot of tracked content plus metadata and parent relationship.
- **Branch:** A movable name pointing to a commit, commonly used for a line of work.
- **`HEAD`:** A reference to the currently checked-out branch or, in detached state, a commit.
- **Remote:** A saved name and URL for another repository, commonly called `origin`.

```text
working directory --git add--> staging area --git commit--> local history
       ^                                                     |
       |                                                     |
       +---------------- checkout/restore -------------------+

local history --git push--> remote repository
local history <--fetch/pull-- remote repository
```

Before every state-changing command, `git status` is a useful first check.

## Core Commands

```bash
git init
git clone <repository-url>
git status
git add .
git commit -m "Add initial CI workflow"
git push
git pull
git log --oneline
git diff
```

- `git init` creates Git metadata for a repository in the current directory. Confirm the directory first to avoid initializing the wrong place.
- `git clone <repository-url>` copies an existing repository into a new local directory and configures a remote, usually `origin`.
- `git status` reports the current branch and differences among working, staged, and recorded content.
- `git add .` stages changes beneath the current directory. Review `git status` and `git diff` first; a narrower path such as `git add README.md` is often safer.
- `git commit -m "..."` records staged contents as a new local commit. The message should explain the change clearly.
- `git push` sends local commits and references to an upstream remote. The first push of a branch may need `git push -u origin branch-name`.
- `git pull` fetches remote changes and integrates them into the current branch according to configuration. Inspect state and understand whether the repository merges or rebases pulls.
- `git log --oneline` shows a compact history view.
- `git diff` shows unstaged changes. `git diff --staged` shows what the next commit would contain.

Commands should not be copied blindly. The same command can be harmless in a practice repository and disruptive on a shared production branch. Check the current directory, branch, status, and intended remote.

## Clone, Fetch, Pull, and Push

**Clone** creates the initial local copy. **Fetch** downloads remote objects and updates remote-tracking references without integrating them into the current branch. This makes `git fetch` useful for inspecting incoming work safely.

**Pull** is a convenience operation that fetches and then integrates, commonly by merge or rebase. Because it can change the working branch, resolve or store local work first. **Push** asks the remote to update a branch or tag from local references. Server protections may reject the update.

Local branches such as `main` are different from remote-tracking references such as `origin/main`. The latter records the last fetched view of the remote branch; it is not a live network folder.

## Status, Diff, and Log

Use `git status` to orient yourself. Use `git diff` before staging and `git diff --staged` before committing. Use `git log --oneline --decorate --graph --all` when branch relationships matter. Together these commands answer where you are, what changed, and how history is connected.

Git tracks content rather than an abstract sequence of keystrokes. A newly created file is untracked until staged. An ignored file is normally omitted from status because a matching `.gitignore` rule tells Git not to suggest it for tracking.

## `.gitignore`

`.gitignore` should list generated, local, or sensitive-by-location patterns that do not belong in version control, such as virtual environments, caches, and local environment files. It does not remove a file already tracked, and it is not a security control. A secret committed before being ignored remains in history and should be revoked.

## Basic Workflow

1. Fetch or pull the agreed starting branch.
2. Create a short-lived branch if the team uses branches.
3. Edit a small, coherent change.
4. Inspect `git status` and `git diff`.
5. Stage only intended files.
6. Inspect `git diff --staged`.
7. Commit with a meaningful message.
8. Push the branch and open a review when appropriate.
9. Act on CI and review feedback.

## Why Git Is Central to CI/CD

Git events commonly trigger automation. The commit hash gives a pipeline a precise source identity. Branch and pull-request context controls which checks run. Tags can identify releases. History links an artifact and deployment back to reviewed code. This traceability depends on preserving useful references and avoiding credentials in commits.

The [TaskOps CI workflow](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) reacts to pull requests and pushes to `main`. The [KubeOps image-release workflow](../../../Projects/2_project/kubeops-gitops/.github/workflows/image-release.yml) reacts to pushes to `main` or a manual request. Inspect these as examples of Git activity becoming pipeline input.

## Practical Exercise

Use a new temporary directory outside important work and spend 15-20 minutes:

1. Run `git init`.
2. Add a `README.md` with one sentence.
3. Inspect, stage, and commit it.
4. Add a second sentence.
5. Inspect the difference before committing.
6. View the history after the second commit.

Safety note: confirm the temporary path before `git init`; do not run the exercise inside this learning repository unless you intend to change it.

## Knowledge Check

1. What is the staging area for?
2. How does `git fetch` differ from `git pull`?
3. What does `HEAD` normally identify?
4. Why should `git diff --staged` be checked before a commit?
5. Does `.gitignore` remove an already committed secret?

<details>
<summary>View answers</summary>

1. It holds the exact proposed contents of the next commit.
2. Fetch downloads and updates remote-tracking references; pull also integrates into the current branch.
3. The currently checked-out branch, or a specific commit in detached state.
4. It reveals exactly what the commit will record and can catch unintended files or changes.
5. No. The secret remains in history and must be revoked and handled appropriately.

</details>

## Navigation

- [Back to Git and Collaboration](../README.md)
- [Next: Commits and History](../02-commits-and-history/)
- [Back to All Learning Materials](../../README.md)
