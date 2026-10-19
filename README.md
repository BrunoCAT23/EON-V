# EON-V

[![Tests](https://github.com/BrunoCAT23/EON-V/actions/workflows/tests.yml/badge.svg?branch=main&event=push)](https://github.com/BrunoCAT23/EON-V/actions/workflows/tests.yml)

EON-V is a modular robot companion runtime. The project is split into brain, voice, vision, memory, behavior, hardware, LLM, tools, and tests so simulation work can move toward real hardware in small steps.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python tools\healthcheck.py
python -m pytest -q
python -m unittest discover
python main.py
```

`python main.py` starts the interactive runtime CLI. Use `help` inside the CLI to see available commands.

## Runtime Modes

Set modes in `.env`.

| Mode | Purpose |
| --- | --- |
| `RUNTIME_MODE=simulation` | Safe default for local development. Uses mock/stub components where configured. |
| `RUNTIME_MODE=voice_only` | Use the voice stack while keeping vision and motion disabled or mocked. |
| `RUNTIME_MODE=vision_only` | Use camera/detection work without real motion. |
| `RUNTIME_MODE=full_robot` | Intended for real hardware after healthcheck and safety checks pass. |

Important component flags:

```env
MIC_MODE=stub
SPEAKER_MODE=stub
STT_MODE=fallback
TTS_MODE=fallback
CAMERA_MODE=stub
DETECTOR_MODE=stub
HARDWARE_MODE=mock
MOTION_ENABLED=true
MOTION_DRY_RUN=true
```

For real movement, keep `MOTION_DRY_RUN=true` until the hardware path is verified.

## Useful Commands

```powershell
python tools\healthcheck.py
python tools\simulate_eon.py
python main.py
```

Inside the runtime:

```text
mode
status
say eon привіт
see person in front of robot
dashboard
self_test
estop test
estop_reset
```

## Recommended Bring-Up Order

1. Run healthcheck and unit tests.
2. Verify Piper TTS with `voice_test`.
3. Verify microphone/VAD with `mic_test`.
4. Verify wake word with `say eon привіт`.
5. Verify camera with `camera_test`.
6. Enable servo/head commands in dry-run first.
7. Enable real motion only after emergency stop and timeout behavior are checked.

## Notes

Memory is stored in `memory/data.json`. The memory manager keeps recent events/dialogue bounded and creates `memory/data.json.bak` before overwriting persistent memory outside sandbox mode.

Use Python 3.10 or newer. The publication checks were run with Python 3.10.0.
The default stub/fallback simulation does not require model downloads, API keys,
a microphone, camera, or physical robot. `healthcheck` checks Piper and Vosk
assets when `TTS_MODE=local_ready` and `STT_MODE=local_ready`, respectively.

The `models/` and `tools/piper/` directories, personal memory, logs, recordings,
and third-party sound recordings are intentionally excluded from Git. Install
external resources separately only if you need their backends; configure their
paths in `.env`. Missing optional sound aliases are unavailable until their
corresponding recordings are installed. Tests generate their own audio fixture.

Before sharing changes, review [publication checks](docs/PUBLISHING.md) and
[asset provenance](docs/ASSETS.md). Never add `.env`, memory records, or local
credentials.

## License

Copyright (C) 2026 BrunoCAT23.

Project software and its documentation are licensed under the GNU General
Public License version 3 only (SPDX: GPL-3.0-only). See [LICENSE](LICENSE).
External models, runtimes and recordings retain their own terms and are not
bundled. CAD files have separate licensing described in [cad/README.md](cad/README.md).

## Mechanical design

The owner-supplied [EON-V Fusion design and preview](cad/README.md) are included
under CC BY 4.0. The archive is unchanged; printability and assembly fit have
not been validated. STEP/STL/3MF exports are not included.
