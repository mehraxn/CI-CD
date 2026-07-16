# YAML Fundamentals

## What YAML Is

YAML ("YAML Ain't Markup Language") is a human-readable data format built from indentation, key-value pairs, and lists. CI/CD tools use it because pipeline configuration is mostly structured data — names, lists of branches, nested job definitions — and YAML expresses that with less visual noise than JSON or XML while remaining machine-parseable.

A YAML file describes *data*. The CI/CD platform then interprets that data against its own schema. Keeping those two layers separate is the single most useful mental model in this lesson.

## Core Structures

**Mapping** (key-value pairs, nested by indentation):

```yaml
application:
  name: task-api
  version: "1.0.0"
```

**Sequence** (a list; each item starts with `- `):

```yaml
branches:
  - main
  - develop
```

**Nested mapping** (mappings inside mappings — the shape of every workflow file):

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
```

Mappings and sequences nest freely: a workflow is a mapping whose `jobs` key holds a mapping of job names, each holding a `steps` sequence of step mappings.

## Scalars: Strings, Numbers, Booleans, Null

Unquoted values are interpreted by type rules: `42` is a number, `true`/`false` are booleans, `null` (or an empty value) is null, and most other text is a string. This convenience creates famous traps:

```yaml
python-version: "3.10"
```

Unquoted, `3.10` is parsed as the *number* 3.1 — the trailing zero disappears, and the pipeline requests a Python version that does not exist. Version-like values, and anything that must stay text (`"yes"`, `"on"`, `"1.0"`), should be quoted. Single quotes are literal; double quotes allow escape sequences. When in doubt, quoting a string is always safe.

Comments start with `#` and run to the end of the line. YAML has no multi-line comment syntax.

## Indentation Rules

Indentation defines structure and must use **spaces, never tabs**. Sibling keys must align exactly. This example is invalid:

```yaml
jobs:
 test:
    runs-on: ubuntu-latest
   steps:
      - run: echo "Invalid indentation"
```

`test` is indented one space, `runs-on` four, and `steps` three — `steps` aligns with nothing, so the parser rejects the file. Consistent two-space indentation, as used in every workflow in this repository, avoids the whole problem class.

## Multiline Blocks

**Literal block** (`|`) preserves newlines — the standard way to write multi-command scripts:

```yaml
run: |
  echo "First command"
  echo "Second command"
```

**Folded block** (`>`) joins lines with spaces — useful for long single-value text:

```yaml
description: >
  This text spans multiple source lines
  but is treated as one folded value.
```

## Less Common Features Worth Recognizing

- **Anchors and aliases** (`&name` / `*name`) let one YAML document reuse a value in several places. GitLab CI/CD configurations sometimes use them; GitHub Actions workflows generally do not support them.
- **Duplicate keys** in one mapping are an error in strict parsers, but some parsers silently keep only the last value — a source of quiet misconfiguration. Never rely on parser leniency.
- **Special characters** — values containing `:`, `#`, `{`, `[`, `*`, `&`, or leading/trailing spaces usually need quoting. GitHub Actions expressions like `${{ github.ref }}` survive unquoted in most positions, but quoting them never hurts.
- **Parser differences** — YAML has revisions and implementation quirks (the `yes`/`no`-as-boolean behavior of YAML 1.1 is the classic example). Pipeline files should stay in the simple, unambiguous subset shown above.

Validation happens at two levels: a generic YAML parser checks syntax, and the platform checks its **schema** — that `jobs`, `steps`, and friends are the right keys with the right shapes. Editors with platform schema support (or GitLab's CI lint endpoint) catch schema errors before a push does.

## Valid YAML Does Not Mean a Valid Pipeline

A file can parse perfectly and still fail as a pipeline:

- The YAML parser accepts any keys — `jbos:` instead of `jobs:` is valid YAML and a broken workflow.
- Platform rules may reject invalid structure: a `needs` reference to a job that does not exist, or a malformed expression.
- Commands may fail at runtime — the platform cannot know that `./scripts/verify.sh` does not exist until a runner tries it.
- Secrets or variables may be unavailable in the event that actually triggers the run.
- A syntactically valid workflow may still be insecure — overly broad permissions or unpinned actions parse just fine.

Syntax, schema, runtime, and security are four separate layers of "valid." Each needs its own check.

## Existing Workflow Evidence

Every YAML feature in this lesson appears in the real workflows. [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) uses nested mappings (`jobs.quality.steps`), sequences (`branches: [main]` in flow style, and the block-style step list), a quoted version (`python-version: "3.12"`), quoted numbers that must stay strings (`exit-code: "1"`), literal blocks (`run: |` for the container smoke test), and comments explaining trigger choices. [TaskOps CD](../../../Projects/1_project/taskops-cicd/.github/workflows/cd.yml) additionally shows a multiline sequence inside a step input (`tags: |`).

## Practical Exercise

Open [TaskOps CI](../../../Projects/1_project/taskops-cicd/.github/workflows/ci.yml) in an editor (read-only) and identify one concrete example of each:

1. A mapping and its nesting depth.
2. A list (block style or flow style).
3. A plain unquoted string.
4. One multiline block and whether it is literal or folded.
5. One quoted version-like value and why the quotes matter.
6. One platform-specific keyword that a generic YAML parser would accept but only GitHub Actions understands.

Write the six findings as notes with line references. Do not modify the file. Target 15–25 minutes.

## Knowledge Check

1. What is the difference between a mapping and a sequence?
2. Why is `python-version: 3.10` a bug while `python-version: "3.10"` is not?
3. Can YAML indentation use tabs?
4. What does the `|` block scalar do, and when is `>` preferred?
5. Give two reasons a syntactically valid YAML file can still be a broken workflow.

<details>
<summary>View answers</summary>

1. A mapping holds named key-value pairs; a sequence holds an ordered list of items introduced by `- `.
2. Unquoted `3.10` parses as the number 3.1, losing the trailing zero; quoting keeps it the literal string "3.10".
3. No — YAML indentation must use spaces; tabs are a syntax error.
4. `|` preserves newlines (multi-command scripts); `>` folds lines into spaces (long single-value prose).
5. The keys may not match the platform schema (a typo like `jbos:`), and runtime problems — missing scripts, unavailable secrets, failing commands — only appear when the pipeline executes. Insecure but parseable configuration is a third layer.

</details>

## Navigation

- [Back to Pipeline as Code and Platforms](../README.md)
- [Previous: Pipeline as Code Fundamentals](../01-pipeline-as-code-fundamentals/)
- [Next: Variables, Contexts, Expressions, and Outputs](../03-variables-contexts-expressions-and-outputs/)
- [Back to All Learning Materials](../../README.md)
