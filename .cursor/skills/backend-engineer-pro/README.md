# backend-engineer-pro

A Claude Agent Skill for strict, specification-driven Python backend engineering with FastAPI and PostgreSQL.

## Workflow preference

This skill intentionally does **not** use test-first development. It requires:
1. Agree and document the specification.
2. Inspect the existing repository.
3. Implement production code against the agreed specification.
4. Review the implementation and run suitable non-test checks.
5. Add test cases only after implementation is complete and the user asks for or approves the testing phase.

This is a deliberate workflow choice, not a claim that tests are unnecessary. Testing remains a recommended separate verification phase.

## Install

For Claude Code, copy this folder into either:

- Project scope: `<your-project>/.claude/skills/backend-engineer-pro/`
- Personal scope: `~/.claude/skills/backend-engineer-pro/`

The folder must contain `SKILL.md` at its root. Restart or reload Claude Code if the skill does not appear. Invoke it by asking Claude to use `backend-engineer-pro`, or let Claude select it based on the description.

For Claude.ai, use the Skills interface if your plan/workspace supports custom Skills and upload the folder as a ZIP. Product availability and UI labels can vary.

## Scope

- FastAPI only
- PostgreSQL only
- Strict production engineering
- Specification-driven development
- Clean architecture and practical SOLID
- OWASP-informed security
- Code review and performance
- Microservices only when justified; modular monolith by default

## Customize

Edit `SKILL.md` and the relevant files under `rules/`, `workflows/`, and `templates/` to match your repository conventions.
