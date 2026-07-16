# Branching Strategies

## Why Strategies Exist

A branching strategy is an agreement about where work starts, how long branches live, how changes are reviewed, and which references represent releasable states. The strategy should support the product's release model and risk controls. A complex diagram does not by itself improve delivery.

Branch duration strongly affects CI/CD. Short-lived branches integrate quickly and usually produce smaller conflicts. Long-lived branches allow extended isolation but delay combined feedback and often require repeated stabilization.

## Comparison

| Strategy | Main idea | Strengths | Weaknesses | Suitable for |
|----------|-----------|-----------|------------|--------------|
| Feature branching | Develop each change on a branch, then merge | Clear review boundary; simple isolation | Branches can become large and stale | Teams using pull requests with short work items |
| GitHub Flow | `main` stays deployable; short branches merge through pull requests | Simple; fits continuous web delivery | Needs strong checks and incomplete-feature control | Many modern services and small teams |
| GitLab Flow | Combines feature branches with environment or release flows | Can reflect staged delivery | More references and policy choices | Teams needing explicit environment/release alignment |
| GitFlow | Uses long-lived `develop` and `main` plus feature, release, and hotfix branches | Formal support for scheduled versioned releases | Complex merges and delayed integration | Some products with parallel supported releases |
| Trunk-based development | Integrate into one trunk at least daily, using tiny or very short branches | Fast feedback; low divergence | Requires discipline, automation, and feature controls | Teams capable of incremental change and strong CI |

No strategy is universally best. Team size, regulatory needs, release cadence, supported versions, repository scale, and test quality all matter.

## Major Patterns

**Feature branching** is a general pattern rather than a complete policy. Its effectiveness depends on branch lifetime and pull-request size. A two-hour branch and a three-month branch create very different integration risk.

**GitHub Flow** normally keeps a protected `main`, creates a descriptive branch, opens a pull request, runs checks and review, merges, and deploys from `main`. It is easy to explain and suits many continuously delivered services.

**GitLab Flow** is a family of approaches that may connect feature work to upstream-first, environment, or release branches. It can represent more complex promotion needs but requires careful rules to avoid uncontrolled branch multiplication.

**GitFlow** typically adds a long-lived `develop` branch, creates release branches for stabilization, and uses hotfix branches from production history. It can support products that prepare distinct release trains, but repeated merges among permanent branches add delay and opportunities for divergence.

**Trunk-based development** asks developers to integrate into the shared trunk at least daily. Teams may commit directly under strict practices or use branches that live hours rather than weeks. Feature flags, branch-by-abstraction, strong automated checks, and small design steps keep incomplete work safe.

## Release and Hotfix Branches

A release branch can isolate maintenance for a supported version while newer development continues. It is justified when parallel version support is real, not as a default waiting room for every release. Changes fixed on a release branch must also reach newer lines when relevant.

A hotfix branch is an urgent branch from the affected production reference. Urgency should not remove review, testing, or traceability. The correction must be reconciled with active development to avoid reintroducing the defect.

## Merge Queues and Feature Flags

A merge queue evaluates proposed changes against a current or predicted target state and merges qualifying work in order. It helps busy repositories where many individually green pull requests can conflict after simultaneous merges.

Feature flags allow incomplete behavior to integrate without becoming available to all users. They support small batches and trunk-based work, but flags need owners, secure configuration, test combinations, and removal plans.

## Choosing a Strategy

Ask:

1. How often can the product release?
2. Must multiple versions receive fixes?
3. How quickly do required checks complete?
4. Can incomplete work be hidden safely?
5. How many concurrent changes reach the same areas?
6. Which history and approval requirements are mandatory?

Choose the simplest strategy that satisfies real constraints. Measure branch age, pull-request lead time, conflict frequency, and failed integrations to see whether it works.

## Recommendation for This Repository

For this learning repository, a practical starting policy is:

- protect `main`;
- use short-lived feature or documentation branches;
- open pull requests;
- require relevant CI checks;
- require review for meaningful changes;
- consistently use squash merge or another selected method; and
- create immutable version tags for releases.

This resembles GitHub Flow. It matches the existing [TaskOps CI trigger](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) and [KubeOps CI trigger](../../../Projects/2_project/kubeops-gitops/.github/workflows/ci.yml), both of which validate pull requests. The actual repository protection settings are not stored in these files, so the recommendation is not a claim that they are enabled.

## Practical Exercise

Compare GitHub Flow and trunk-based development for a five-person team maintaining TaskOps. In a short table, assess branch lifetime, review, incomplete features, CI expectations, and release behavior. Recommend one and state the assumptions behind the choice.

## Knowledge Check

1. Why do long-lived branches usually slow integration feedback?
2. What discipline does trunk-based development require?
3. When can a release branch be justified?
4. Why is GitFlow not automatically the safest strategy?
5. What problem does a merge queue address?

<details>
<summary>View answers</summary>

1. They diverge from shared work and delay testing of combined changes.
2. Tiny changes, frequent integration, strong CI, and safe control of incomplete behavior.
3. When the product genuinely maintains or stabilizes a separate supported version.
4. Its extra branches create more merges, delay, and coordination work.
5. It tests and orders changes against an evolving target so separately green changes do not break it when combined.

</details>

## Navigation

- [Back to Git and Collaboration](../README.md)
- [Previous: Pull Requests and Code Review](../04-pull-requests-and-code-review/)
- [Next: Tags, Versioning, and Releases](../06-tags-versioning-and-releases/)
- [Back to All Learning Materials](../../README.md)
