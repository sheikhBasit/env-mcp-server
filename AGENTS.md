# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Cursor, GitHub Copilot, etc.)
working in this repository.

## Project
MCP server for environment variable management — read, validate, diff `.env` files with automatic secret masking. Built with FastMCP.

## Code Style
- Python 3.11+
- Follow existing patterns in the codebase before adding new ones
- Use type hints on all public functions

## Security Rules (CRITICAL)
- The secret masking regex in `env_tools.py` must ALWAYS be applied before returning any env value
- Never return raw values for keys matching: `secret|password|passwd|token|key|api_key|private|credential|auth|jwt|cert|seed`
- Tests must assert that masked values never appear unmasked in output

## Testing
- Run tests before committing: `pytest`
- All new tools require tests in `tests/`

## Commits
- Use conventional commits: `feat:`, `fix:`, `chore:`, `docs:`
- No WIP commits to main

## What NOT to do
- Do not add dependencies without updating `pyproject.toml`
- Do not weaken or bypass the secret masking — this is a security boundary
