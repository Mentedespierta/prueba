# Repository Guidelines

This repo contains a prototype legal case management system using Streamlit and FAISS.

## Coding conventions
- Use Python 3.8+.
- Keep functions small and documented with docstrings.
- Use `snake_case` for variables and functions.

## Branches
- Work directly on `main`. Create commits with clear messages.

## Testing
- Run `pytest` before committing if tests exist.
- Tests are located in `tests/` and should not require network access.

## Data
- Place processed files under `procesado/`.
- Large files should not be committed to the repository.
