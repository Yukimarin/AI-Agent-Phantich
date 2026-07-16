---
name: super-memory
description: Use when starting any new task, subagent invocation, or conversation turn to retrieve context from past sessions, or when completing a milestone or encountering a key learning to save persistent context and prevent amnesia.
---

# Super Memory Skill

## Overview

Super Memory is a mechanism to persist critical project context, lessons learned, and guidelines across sessions, ensuring the agent doesn't repeat mistakes or lose context.

## When to Use

- At the start of every session or new task to read past memories and preferences.
- When you run into a bug or error and find a specific fix that is not obvious.
- When the user guides you to a styling, design, or behavioral preference that you must remember.
- At the end of every session or task to write down a summary of changes, unresolved questions, and the next steps.

## Core Pattern

### 1. Reading from Memory (At Start)
Locate and view `docs/super_memory.md` to load user preferences, lessons learned, and system parameters.

### 2. Updating Memory (At End or Key Learning)
Append or update the relevant section of `docs/super_memory.md` using clean Markdown tables or bullet points.

## Quick Reference

| Action | Target File | Purpose |
| :--- | :--- | :--- |
| Read Memory | `docs/super_memory.md` | Retrieve historical decisions, preferences, and lessons. |
| Write Memory | `docs/super_memory.md` | Record newly discovered rules, bugs, styles, or session summaries. |

## Implementation

```markdown
# Super Memory

## 1. User Preferences
- Preferred styling: sleek glassmorphism, HSL custom colors.
- Communication style: Vietnamese, concise, direct.

## 2. Lessons Learned & Bug Fixes
- [2026-07-04] SQLite DB query format for training KPI should use `auto_rpoints` table for KS25.
- [2026-07-04] Do not run nested subagent code directly in python; coordinate via Antigravity instead.

## 3. Current Session State
- Session ID: 80ef82ea-69fb-4e9f-8432-ad3a1e4e8b34
- Last completed task: Installed Super Memory skill.
```

## Common Mistakes

- **Forgetting to check memory at the start:** Leads to repeating past errors or asking questions the user already answered.
- **Overwriting the whole file without preserving history:** Use selective replacement or appending to keep past learnings intact.
- **Recording trivial logs:** Keep memory focused on rules, patterns, preferences, and key architectural notes.
