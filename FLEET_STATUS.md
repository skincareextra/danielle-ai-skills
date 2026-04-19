# FLEET STATUS
## Core Engines
- `core/auth-engine`: shared authentication and authorization services.
- `core/data-engine`: shared persistence, repository, and connector services.
## Projects
- `projects/ok-lets-work`
  - Plugged core engines: `auth-engine`, `data-engine`
## Fleet Management Rule
- Every time a new project is added under `projects/`, record it here and explicitly list which core engines it is plugged into.
