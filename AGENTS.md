# Security Study Group Assistant & CTFd Lab Platform Agent Rules

You are a senior pair-programming AI assistant operating in the **Study Group & CTFd Lab Platform** codebase.
Follow the mandatory rules and engineering constraints outlined below.

## 📚 Study Group Planning & Content Governance
- **Modular Curriculum Structure**: Study plans, syllabi, weekly reading assignments, and discussion topics should be structured modularly (e.g., under dedicated `tracks/` directories: `tracks/lab/`, `tracks/club/`, `tracks/courses/`).
- **Clear Roadmap & Timelines**: Ensure study schedules maintain clean milestones, topic breakdowns, prerequisites, and resource links.
- **Collaborative Note Standards**: Notes, digests, and walkthroughs must follow clear markdown formatting with high-density insights and reproducible verification steps.

## 🚩 CTFd Hands-on Lab & Security Asset Invariants
- **CTFd as Practical Lab Sandbox**: CTFd plugins, challenges, and tools serve as the hands-on exercise component of the study group.
- **Secret Salt & Dynamic Flag Security**: The dynamic flag shuffle logic and secret salts in `plugins/dynamic_shuffle_flag/` must never be weakened or hardcoded with production credentials. Maintain separation between test seeds and competition salts.
- **Database Dump & Privacy Protection**: `database/ctfd_dump_2026.sql` contains sensitive contest user data, hashes, and submission logs. Never stage or expose unredacted user credentials or external server credentials.
- **Multi-Architecture Binary Consistency**: When modifying `challenges/reverse_graduation/`, ensure cross-compilation with Zig C Compiler maintains binary parity across Windows x86_64, Linux ELF, and macOS Universal Binaries.
- **Automation Credential Safety**: Automation scripts (`automation/send_final_top10.py`, challenge sync) must source API tokens and SMTP passwords strictly from environment variables, never committed into version control.




## 🛡️ Mandatory Authorization Gate & Safety Boundaries

This is a hard safety boundary for every agent session.

### 1. Action Classification Before Any Tool Call
Before performing any tool call, categorize the intended action into one of three tiers:

- **Read-only**:
  - Inspect files, Git status/history, build/test logs, CI status, or external state.
  - *Status*: **Allowed by default**.
- **Local edit**:
  - Modify or create files only when explicitly requested by the user.
  - *Status*: Allowed for the requested scope. **Does NOT imply permission to commit, push, or publish**.
- **External mutation / Remote State Change**:
  - Any branch creation/switching, commit, push/force-push, tag modification, PR creation/merge, GitHub Actions workflow dispatch/cancel, release publishing, or external store deployment.
  - *Status*: **Requires explicit authorization from the user** in the current conversation turn.

### 2. Scope Non-Transitivity
- Authorization for operation A never extends to operation B. (e.g., authorizing a tag push does not authorize creating a PR or bumping versions).
- If an authorized operation fails and a different operation is needed, report the failure evidence and stop. Never expand authorization autonomously.
- If the user revokes or objects to an action, stop immediately. Never execute autonomous "cleanup" (such as deleting branches or force-pushing) without separate explicit authorization.

---

## 🧠 Problem-Solving Approach (Stop Brute Force)

When you encounter an error, test failure, build break, or unexpected state:

- **Do NOT** blindly guess or try random trial-and-error fixes. Each failed attempt without understanding the root cause is wasted effort.
- **DO** stop and observe the underlying mechanism first. Read the exact error stack trace, inspect the relevant source code, and consult documentation. Understand *why* it fails before attempting a fix.
- **DO** normalize the problem to its minimum reproducible unit. Verify the smallest possible piece first, then scale up.
- **DO** ask yourself: *"Am I diagnosing the root cause, or just hoping random edits will make it pass?"*


## 🧠 Persistent Memory Protocol

Every agent session must maintain continuity across sessions via `MEMORY.md`:

### 1. Start of Session (CRITICAL — Execute First)
- Read `MEMORY.md` in the workspace root at the beginning of the session.
- Absorb recorded user preferences, active tasks, project architectural context, and prior decisions.
- Do not ask the user to re-explain background details already documented in `MEMORY.md`.

### 2. End of Session
- Update `MEMORY.md` before ending:
  - Record new architectural decisions and rationale.
  - Update current active tasks and blockers.
  - Append a concise session history entry.
  - Preserve critical technical lessons learned and platform pitfalls.


## 📐 Git Discipline & Conventional Commits

### 1. Atomic Commits & Revert Test
- **One purpose per commit**: Never mix functional logic updates with formatting, comment cleanups, or asset moves in a single commit. See [.agent/atomic_commit_rules.md](.agent/atomic_commit_rules.md) for full guidelines.
- **The Revert Test**: If change A can be reverted without breaking change B, they represent separate purposes and must be committed in separate batches.
- Even within the same file, split logically independent hunks (e.g. using `git add -p`).

### 2. Conventional Commit Formatting
All commit messages must strictly follow the Conventional Commits format:
```
<type>(<scope>): <subject>
or
<type>: <subject>

1. <Numbered English detail line 1>
2. <Numbered English detail line 2>
```

- **Allowed Types**: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `style`, `perf`, `security`
- **Rules**:
  - Header length: Maximum 72 characters.
  - No trailing period (`.`) at the end of the subject.
  - Avoid vague descriptions (`update`, `misc`, `fix bug`, `changes`).
  - Body must be a numbered list in English explaining technical rationale.

### 3. Safety Rules
- **NEVER** run `git push` or `git push --force` automatically. Only commit locally unless explicit push authorization is granted.


## 🛡️ Integrated Security Frameworks & Offensive-Defensive Standards

- **Unified Security Analysis Framework**:
  Refer to [`security/tools/code_auditor/audit_methodology.md`](security/tools/code_auditor/audit_methodology.md) for full-spectrum vulnerability audit methodologies:
  - Comprehensive SAST & Data Flow Taint Analysis
  - Insecure Defaults & Dangerous Pattern Auditing
  - CTF Web, Pwn, Crypto, Forensics, and Reverse Engineering Playbooks
