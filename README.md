# EON-V

EON-V is a modular robot companion runtime. The project is split into brain, voice, vision, memory, behavior, hardware, LLM, tools, and tests so simulation work can move toward real hardware in small steps.

## Quick Start

```powershell
python -m pip install -r requirements.txt
python tools\healthcheck.py
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
