from __future__ import annotations

import argparse
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from runtime_app import RuntimeApp


@dataclass
class Scenario:
    name: str
    commands: list[str]


SCENARIOS = [
    Scenario(
        name="basic_voice",
        commands=[
            "say hello without wake word",
            "say eon привіт",
            "say eon статус",
            "say eon подумай",
        ],
    ),
    Scenario(
        name="memory_and_people",
        commands=[
            "meet serhii",
            "say eon запам'ятай що любить робототехніку",
            "say eon що ти знаєш про serhii",
            "see serhii person in front of robot",
        ],
    ),
    Scenario(
        name="vision",
        commands=[
            "see empty room",
            "see unknown person near robot",
            "see cat on the floor",
            "see dog near serhii",
        ],
    ),
    Scenario(
        name="state_and_runtime",
        commands=[
            "status",
            "auto_on",
            "run_steps 3",
            "idle_auto",
            "run_all",
            "auto_off",
        ],
    ),
    Scenario(
        name="companion_features",
        commands=[
            "meet serhii",
            "profile_set_name serhii Сергій",
            "profile_add_date serhii birthday 15-03",
            "profile serhii",
            "teach улюблений_режим = автономний компаньйон",
            "remind_in 2 перевірити заряд",
            "auto_on",
            "run_steps 2",
            "run_all",
            "head left",
            "head center",
            "safety_status",
            "diagnostics",
            "event_log",
            "dashboard",
            "auto_off",
        ],
    ),
    Scenario(
        name="safety_and_unknowns",
        commands=[
            "",
            "unknown_command",
            "skill missing_skill",
            "behavior missing_animation",
            "run_all",
        ],
    ),
]


def run_scenario(app: RuntimeApp, scenario: Scenario) -> tuple[int, list[str]]:
    failures = []

    print(f"\n=== Scenario: {scenario.name} ===")

    for command in scenario.commands:
        print(f"\n> {command or '<empty>'}")
        try:
            app.handle_command(command)
        except Exception:
            failures.append(command)
            traceback.print_exc()

    return len(failures), failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run EON-V simulated scenarios.")
    parser.add_argument(
        "--scenario",
        choices=[scenario.name for scenario in SCENARIOS],
        help="Run a single scenario.",
    )
    args = parser.parse_args(argv)

    selected = SCENARIOS
    if args.scenario:
        selected = [scenario for scenario in SCENARIOS if scenario.name == args.scenario]

    app = RuntimeApp()
    total_failures = 0
    failed_commands = {}

    for scenario in selected:
        failure_count, failures = run_scenario(app, scenario)
        total_failures += failure_count
        if failures:
            failed_commands[scenario.name] = failures

    print("\n=== Simulation summary ===")
    print(f"Scenarios: {len(selected)}")
    print(f"Failures: {total_failures}")
    print(f"Queued actions after simulation: {len(app.brain.action_queue.snapshot())}")
    print(f"Final state: {app.brain.state_manager.get_state()}")
    print(f"Current mood: {app.brain.current_mood}")
    print(f"Known people: {list(app.brain.memory_manager.get_people().keys())}")
    print(f"Known pets: {list(app.brain.memory_manager.get_pets().keys())}")

    if failed_commands:
        print(f"Failed commands: {failed_commands}")
        return 1

    print("Simulation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
