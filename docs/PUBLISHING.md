# Local publication checklist

No GitHub push or visibility change is part of local preparation.

1. Review `git status --short`, `git diff`, and `git diff --cached`.
2. The owner accepted the personal email in the existing 11 commits; preserve
   that history. New commits use the owner's GitHub noreply address.
3. The owner confirmed rights and selected GPL-3.0-only for their software and
   CC BY 4.0 for their CAD model. Keep third-party resources excluded.
4. Confirm `.env`, personal memory and its backups, logs, recordings, models,
   Piper binaries, archives and private credential files remain ignored.
   Only `memory/__init__.py` and `memory/memory_manager.py` belong in Git.
5. Run `python -m pytest -q` and `python -m unittest discover` in simulation
   with `MEMORY_SANDBOX=true`, stub inputs/outputs, mock hardware, dry-run
   motion, and both cloud/local LLM services disabled. Run healthcheck too.
6. Validate a fresh checkout without ignored files. Local models and sounds
   must not be needed for fallback simulation or the automated test suite.
7. Stage only explicitly reviewed file paths. Never use `git add .`.
8. Inspect the final staged snapshot for secrets and private data, then make
   a local commit. Confirm destination and visibility with the owner before
   any push or remote repository creation.

Dependencies currently have no lock file. Passing checks in the existing
Python environment does not prove reproducible installation on a fresh machine.
Real hardware, microphone/camera, cloud LLM and downloaded model backends need
separate validation before use.
