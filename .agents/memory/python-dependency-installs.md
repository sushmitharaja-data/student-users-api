---
name: Python dependency installs
description: Installing Python packages in this Nix-backed Replit workspace.
---

When `installLanguagePackages` falls back to system `pip`, installation may fail because `pip` is absent and the Nix Python is externally managed. The project-local `.pythonlibs` environment can still be managed with `uv`.

**Why:** System Python is immutable here; installing packages directly into it fails.

**How to apply:** After the package callback fails for this reason, use `uv pip install --python .pythonlibs/bin/python <packages>` and keep the project's reproducible dependencies listed in `requirements.txt`.
