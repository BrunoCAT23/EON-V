from __future__ import annotations

from html import escape
from pathlib import Path


def build_dashboard(brain, output_path: Path) -> Path:
    state = escape(str(brain.state_manager.get_state()))
    emotion = escape(str(brain.emotion_engine.get_emotion()))
    mood = escape(str(brain.current_mood))
    people = ", ".join(brain.memory_manager.get_people().keys()) or "none"
    pets = ", ".join(brain.memory_manager.get_pets().keys()) or "none"
    actions = escape(str(brain.action_queue.snapshot()))
    reminders = escape(str(brain.schedule_manager.snapshot()))
    hardware = brain.hardware_manager.get_status()
    hardware_mode = escape(str(hardware.get("mode")))
    safety = hardware.get("safety", {})
    safety_status = escape(str(safety))
    wake_status = escape(str(getattr(brain, "last_voice_intent", "ready")))
    context = escape(str(brain.memory_manager.get_context_memory()))
    events = brain.event_log.recent(30)

    event_rows = "\n".join(
        "<tr>"
        f"<td>{escape(entry['time'])}</td>"
        f"<td>{escape(entry['category'])}</td>"
        f"<td>{escape(entry['message'])}</td>"
        f"<td>{escape(str(entry['payload']))}</td>"
        "</tr>"
        for entry in events
    )

    html = f"""<!doctype html>
<html lang="uk">
<head>
  <meta charset="utf-8">
  <title>EON-V Dashboard</title>
  <style>
    body {{ margin: 0; font-family: Segoe UI, Arial, sans-serif; background: #f4f6f8; color: #18202a; }}
    header {{ background: #18202a; color: white; padding: 18px 24px; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 24px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; }}
    .card {{ background: white; border: 1px solid #d8dee6; border-radius: 8px; padding: 14px; }}
    .label {{ color: #5f6b7a; font-size: 12px; text-transform: uppercase; }}
    .value {{ font-size: 20px; margin-top: 6px; }}
    table {{ width: 100%; border-collapse: collapse; background: white; margin-top: 16px; }}
    th, td {{ border: 1px solid #d8dee6; padding: 8px; text-align: left; vertical-align: top; }}
    th {{ background: #edf1f5; }}
    code {{ white-space: pre-wrap; }}
  </style>
</head>
<body>
  <header><h1>EON-V Dashboard</h1></header>
  <main>
    <section class="grid">
      <div class="card"><div class="label">State</div><div class="value">{state}</div></div>
      <div class="card"><div class="label">Emotion</div><div class="value">{emotion}</div></div>
      <div class="card"><div class="label">Mood</div><div class="value">{mood}</div></div>
      <div class="card"><div class="label">Autonomous</div><div class="value">{brain.life_state.is_enabled()}</div></div>
    </section>
    <section class="grid" style="margin-top:12px">
      <div class="card"><div class="label">People</div><div>{escape(people)}</div></div>
      <div class="card"><div class="label">Pets</div><div>{escape(pets)}</div></div>
      <div class="card"><div class="label">Queue</div><code>{actions}</code></div>
      <div class="card"><div class="label">Reminders</div><code>{reminders}</code></div>
    </section>
    <section class="grid" style="margin-top:12px">
      <div class="card"><div class="label">Hardware</div><div>{hardware_mode}</div></div>
      <div class="card"><div class="label">Wake / Voice</div><code>{wake_status}</code></div>
      <div class="card"><div class="label">Safety</div><code>{safety_status}</code></div>
      <div class="card"><div class="label">Memory Context</div><code>{context}</code></div>
    </section>
    <h2>Event Log</h2>
    <table>
      <thead><tr><th>Time</th><th>Category</th><th>Message</th><th>Payload</th></tr></thead>
      <tbody>{event_rows}</tbody>
    </table>
  </main>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path
