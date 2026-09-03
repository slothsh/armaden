## MANDATORY: Local Code Search/Traversal

Always use the `graphify` skill to query and search for any local code. Only revert to manual grepping as a last resort.

## MANDATORY: Use td for Task Management

Run td usage --new-session at conversation start (or after /clear). This tells you what to work on next.

Sessions are automatic (based on terminal/agent context). Optional:
- td session "name" to label the current session
- td session --new to force a new session in the same context

Use td usage -q after first read.

When the user asks you to create an epic in `td`, **always** add the epic and its tasks with these guidelines:

- Use **VERY** elaborate descriptions for each task on the epic using the --description flag.
- Add relevant labels to each task using the --label task. 2-5 is more than enough.
- Keep the name of the epic concise and relevant to the overall theme of the tasks.

## MANDATORY: Worktree Management

Whenever the user gives you an instruction to work on a git worktree, use the `wt` (worktrunk) command to manage worktrees.

Use the `wt-switch-create` skill for managing worktrees and/or the `worktrunk` skill for more detailed information on how to use the `wt` tool.

## MANDATORY: Code Comment Conventions

Do NOT add documentation comments to ANY code. This will only be required on request from the user.

## MANDATORY: Git Rules

NEVER stage, commit, pull or push any changes EVER. This will only be required on request from the user.

**Note**: When the user has asked you to make commits, then the `graphify` post-commit hook will run after a commit has been made. Always commit these `graphify` artifacts as a new, separate commit with message `chore: commit graph`.

NEVER use squash commit merges unless explicitly asked to do so by the user.

## MANDATORY: General Development Guidelines

- Use absolute imports for all project-local modules. Do not introduce relative imports.
- Arrange module dependencies so runtime code does not need `TYPE_CHECKING`-only imports to resolve cycles. Prefer dependency inversion through protocols, smaller independent modules, or a deliberate lower-level dependency boundary.
- Separate protocols/interfaces from concrete runtime implementations. Keep protocols focused and composable by concern rather than creating one broad god protocol when smaller contracts are practical.
- Concrete implementations must inherit the protocol they implement, and every inherited implementation must be marked with `@override`.
- Do not use `Self` in static methods. Use `Self` for fluent instance APIs and other contexts where the type checker can infer the implementing type; use an explicit protocol or generic abstraction for static APIs.
- Keep one cohesive component per module and name modules after their primary component. Move domain-specific helpers into the narrowest appropriate namespace instead of adding them to general-purpose support modules.
- Isolate related exceptions, marker/tag types, reflection utilities, collection utilities, and other support concerns into dedicated modules when they have distinct responsibilities.
- Use modern Python type syntax: builtin generics (`list[T]`, `dict[K, V]`), union operators (`T | None`), and `type Alias = ...` declarations for type aliases. Avoid `Any` and legacy aliases such as `Dict`, `List`, `Tuple`, and `Optional`.
- Annotate class attributes explicitly, including attributes initialized in constructors. Use typed narrowing and type guards at dynamic boundaries; use `cast` only when the runtime invariant is established and cannot be expressed through narrowing.
- Treat basedpyright as a required quality gate. Every touched module must finish with zero errors and zero warnings; do not silence diagnostics without addressing the underlying type design.
- Use snake_case for method names. Keep methods alphabetically ordered within focused protocol and runtime classes, with two blank lines between adjacent class methods.
- Work incrementally and preserve behavior: trace dependencies recursively, make one architectural decision at a time, and validate each boundary with focused checks before moving on.
