## MANDATORY: Local Code Search/Traversal

Always use the `graphify` skill to query and search for any local code. Only revert to manual grepping as a last resort.

## MANDATORY: Use td for Task Management

Run td usage --new-session at conversation start (or after /clear). This tells you what to work on next.

Sessions are automatic (based on terminal/agent context). Optional:
- td session "name" to label the current session
- td session --new to force a new session in the same context

Use td usage -q after first read.

## MANDATORY: Code Comment Conventions

Do NOT add documentation comments to ANY code. This will only be required on request from the user.

## MANDATORY: Git Rules

NEVER stage, commit, pull or push any changes EVER. This will only be required on request from the user.
