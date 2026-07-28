---
name: super-memory
description: Use when starting any new task, subagent invocation, or conversation turn to retrieve context from past sessions, or when completing a milestone or encountering a key learning to save persistent context and prevent amnesia.
---

# Super Memory Skill

## Overview

Super Memory is a mechanism to persist critical project context, lessons learned, and guidelines across sessions, ensuring the agent doesn't repeat mistakes or lose context.

## State-Based Paradigm (CRITICAL)

**Super Memory is a State Document (like a Wikipedia page), NOT a chronological log.**
Do **NOT** append daily logs or meeting minutes.
When you learn something new, update the relevant section **in-place**.
When a task is done, **remove** it from the Active Task section. Do not leave a trace of completed tasks.

**CRITICAL RULE: USER APPROVAL REQUIRED**
You must NEVER autonomously overwrite or add new decisions to the Core Logic, User Preferences, or Current State without the user's explicit consent.
When you discover a new rule or want to update the State, you must first ask the user: "Tôi có nên cập nhật điều này vào Super Memory không?". Only proceed to edit `Super Memory.md` if they say yes.

## When to Use

- At the start of every session or new task to read past memories and preferences.
- When you run into a bug or error and find a specific fix that is not obvious.
- When the user guides you to a styling, design, or behavioral preference that you must remember.
- To update the Active Task section with your current unresolved task.

## Quick Reference

| Action | Target File | Purpose |
| :--- | :--- | :--- |
| Read Memory | `docs/super_memory.md` or `docs/Super Memory.md` | Retrieve historical decisions, preferences, and lessons. |
| Write Memory | `docs/super_memory.md` or `docs/Super Memory.md` | OVERWRITE/UPDATE newly discovered rules, bugs, styles, or active tasks. |

## Implementation Structure

```markdown
# Super Memory

## 1. User Preferences
- (Overwrite/update with new preferences)

## 2. Core Logic
- (Overwrite/update with new rules)

## 3. Current State
- (Overwrite/update with current org chart, system states)

## 4. Active Task
- (Replace with the current unresolved task. Delete when finished.)
```

## Common Mistakes

- **Appending chronological logs:** DO NOT write "[Date] Did this...". This bloats the context. Update rules in-place instead.
- **Forgetting to check memory at the start:** Leads to repeating past errors or asking questions the user already answered.
- **Leaving completed tasks in Active Task:** Always wipe the Active Task section when a task is completed.
