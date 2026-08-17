from state_manager import StateManager
from event_bus import EventBus
from personality.emotions import EmotionEngine
from personality.personality_engine import PersonalityEngine
from personality.emotional_dynamics import EmotionalDynamics
from personality.mood_engine import MoodEngine
from memory.memory_manager import MemoryManager

from brain.actions import ActionExecutor
from brain.planner import Planner
from brain.context_manager import ContextManager
from brain.social_context import SocialContext
from brain.action_queue import ActionQueue
from brain.scheduler import Scheduler
from brain.life_state import LifeState
from brain.autonomous_loop import AutonomousLoop
from brain.timer_manager import TimerManager
from brain.reactive_triggers import ReactiveTriggers
from brain.presence_model import PresenceModel
from brain.perception_fusion import PerceptionFusion
from brain.personal_knowledge import PersonalKnowledge
from brain.dialogue_memory import DialogueMemory
from brain.needs_engine import NeedsEngine
from brain.goal_engine import GoalEngine
from brain.goal_executor import GoalExecutor
from brain.stimulus_tracker import StimulusTracker
from brain.attention_system import AttentionSystem
from brain.curiosity_engine import CuriosityEngine
from brain.learning_engine import LearningEngine
from brain.preference_model import PreferenceModel
from brain.relationship_model import RelationshipModel
from brain.bond_engine import BondEngine
from brain.attachment_engine import AttachmentEngine
from brain.companion_behavior import CompanionBehavior
from brain.pet_model import PetModel
from brain.pet_play_engine import PetPlayEngine
from brain.pet_behavior_engine import PetBehaviorEngine
from brain.safety_layer import SafetyLayer
from brain.runtime_orchestrator import RuntimeOrchestrator
from brain.life_loop import LifeLoop
from brain.perception_sync import PerceptionSync
from brain.stimulus_fusion import StimulusFusion
from brain.event_log import EventLog
from brain.schedule_manager import ScheduleManager

from skills.skill_manager import SkillManager
from behaviors.behavior_engine import BehaviorEngine
from hardware.simulation_hardware import SimulationHardware
from llm.llm_manager import LLMManager
from hardware_interfaces.hardware_backend import HardwareBackend


class Brain:
    def __init__(self, hardware_manager: HardwareBackend | None = None) -> None:
        self.state_manager = StateManager()
        self.event_bus = EventBus()
        self.emotion_engine = EmotionEngine()
        self.memory_manager = MemoryManager()

        self.emotional_dynamics = EmotionalDynamics()
        self.mood_engine = MoodEngine()
        self.current_mood = "calm"

        self.hardware_manager = hardware_manager or SimulationHardware()
        self.action_executor = ActionExecutor(self.hardware_manager)

        self.action_queue = ActionQueue()
        self.scheduler = Scheduler(self, self.action_queue)

        self.planner = Planner()
        self.context_manager = ContextManager()
        self.social_context = SocialContext()

        self.skill_manager = SkillManager()
        self.behavior_engine = BehaviorEngine()

        self.life_state = LifeState()
        self.autonomous_loop = AutonomousLoop()

        self.timer_manager = TimerManager()
        self.reactive_triggers = ReactiveTriggers()

        self.presence_model = PresenceModel()
        self.perception_fusion = PerceptionFusion()

        self.personal_knowledge = PersonalKnowledge()
        self.dialogue_memory = DialogueMemory()
        self.llm_manager = LLMManager()

        self.needs_engine = NeedsEngine()
        self.goal_engine = GoalEngine()
        self.goal_executor = GoalExecutor()
        self.current_goal = None
        self.last_voice_intent = None

        self.stimulus_tracker = StimulusTracker()
        self.attention_system = AttentionSystem()
        self.curiosity_engine = CuriosityEngine()
        self.current_curiosity = None

        self.learning_engine = LearningEngine()
        self.preference_model = PreferenceModel()
        self.relationship_model = RelationshipModel()
        self.bond_engine = BondEngine()

        self.attachment_engine = AttachmentEngine()
        self.companion_behavior = CompanionBehavior()

        self.pet_model = PetModel()
        self.pet_play_engine = PetPlayEngine()
        self.pet_behavior_engine = PetBehaviorEngine()

        self.runtime_orchestrator = RuntimeOrchestrator()
        self.life_loop = LifeLoop(self)

        self.perception_sync = PerceptionSync()
        self.stimulus_fusion = StimulusFusion()

        self.safety_layer = SafetyLayer()
        self.event_log = EventLog()
        self.schedule_manager = ScheduleManager()

        self.personality_engine = PersonalityEngine(
            self.memory_manager.get_robot_profile()
        )

        self.timer_manager.set_timer("idle_behavior", interval=3, current_tick=0)
        self.timer_manager.set_timer("social_ping", interval=5, current_tick=0)

        print("[BRAIN] EON-V brain initialized")
        print(f"[PERSONALITY] {self.personality_engine.describe()}")

    def refresh_attachment_style(self, person_name: str | None) -> None:
        if not person_name:
            return

        relationship = self.relationship_model.get_relationship(self, person_name)
        style = self.attachment_engine.derive_attachment_style(relationship)
        self.memory_manager.update_attachment_style(person_name, style)

    def trigger_emotion(self, emotion: str, amount: float = 0.4) -> None:
        self.emotional_dynamics.trigger(emotion, amount)
        self.current_mood = self.mood_engine.derive_mood(
            self.emotional_dynamics.get_levels()
        )

    def execute_single_action(self, action: dict) -> None:
        action_type = action.get("type")
        value = action.get("value", "")

        if action_type == "set_state":
            self.state_manager.set_state(value)
            return

        if action_type == "gentle_track":
            print("[SAFETY_ACTION] Gentle tracking active")
            return

        if action_type == "soft_idle":
            print("[SAFETY_ACTION] Soft idle behavior active")
            return

        self.action_executor.execute([action])

    def enqueue_actions(self, actions: list[dict]) -> None:
        safe_actions = self.safety_layer.filter_actions(self, actions)
        for action in safe_actions:
            self.event_log.record("action_queued", action.get("type", "unknown"), action)
        self.action_queue.add_actions(safe_actions)

    def run_next_action(self) -> None:
        next_action = self.action_queue.pop_next()

        if not next_action:
            print("[SCHEDULER] No actions to run")
            return

        print(f"[SCHEDULER] Running action: {next_action}")
        self.event_log.record("action_run", next_action.get("type", "unknown"), next_action)
        self.execute_single_action(next_action)

    def run_all_actions(self) -> None:
        if not self.action_queue.has_actions():
            print("[SCHEDULER] Queue is empty")
            return

        while self.action_queue.has_actions():
            self.run_next_action()

    def process_event(self, event: str) -> None:
        event = event.strip().lower()

        if not event:
            print("[BRAIN] Empty event")
            return

        if event == "run":
            self.run_next_action()
            return

        if event == "run_all":
            self.run_all_actions()
            return

        if event == "queue_status":
            print(f"[QUEUE] Current queue: {self.action_queue.snapshot()}")
            return

        if event == "idle_auto":
            actions = self.behavior_engine.generate_idle_behavior(self)
            self.enqueue_actions(actions)
            return

        if event == "auto_on":
            self.life_state.enable()
            return

        if event == "auto_off":
            self.life_state.disable()
            return

        if event == "life_start":
           self.life_loop.start()
           return

        if event == "life_stop":
           self.life_loop.stop()
           return

        if event == "step":
           self.runtime_orchestrator.step(self)
           return

        if event == "tick":
            if self.life_state.is_enabled():
                self.autonomous_loop.tick(self)
            else:
                print("[AUTO_LOOP] Autonomous mode is disabled")
            return

        if event == "update":
            if not self.life_state.is_enabled():
                print("[UPDATE] Autonomous mode is disabled")
                return

            self.life_state.next_tick()
            current_tick = self.life_state.get_tick()
            print(f"[UPDATE] Tick advanced to {current_tick}")

            self.needs_engine.update()

            presence_actions = self.perception_fusion.maintain_presence(self)
            reactive_actions = self.reactive_triggers.evaluate(self)

            goal = self.goal_engine.decide_goal(self)

            goal_actions = []
            if goal:
                print(f"[GOAL] Selected goal: {goal}")
                self.current_goal = goal
                goal_actions = self.goal_executor.execute(self, goal)
            else:
                self.current_goal = None

            combined_actions = []
            combined_actions.extend(presence_actions)
            combined_actions.extend(reactive_actions)
            combined_actions.extend(goal_actions)

            if combined_actions:
                self.enqueue_actions(combined_actions)
            else:
                print("[UPDATE] No reactive actions generated")
            self.handle_check_reminders()
            return

        if event.startswith("behavior "):
            behavior_name = event.replace("behavior ", "", 1).strip()
            actions = self.behavior_engine.run_animation(behavior_name, self)
            self.enqueue_actions(actions)
            return

        self.event_bus.emit(event)
        self.memory_manager.remember(f"event:{event}")
        self.event_log.record("event", event)
        self.context_manager.set_last_system_event(event)

        if event == "status":
            self.print_status()
            return

        if event == "event_log":
            self.print_event_log()
            return

        if event == "diagnostics":
            self.handle_diagnostics()
            return

        if event == "safety_status":
            self.handle_safety_status()
            return

        if event == "schedule_status":
            self.handle_schedule_status()
            return

        if event.startswith("remind_in "):
            self.handle_remind_in(event)
            return

        if event == "check_reminders":
            self.handle_check_reminders()
            return

        if event.startswith("profile_set_name "):
            self.handle_profile_set_name(event)
            return

        if event.startswith("profile_add_date "):
            self.handle_profile_add_date(event)
            return

        if event.startswith("profile "):
            self.handle_profile(event)
            return

        if event.startswith("teach "):
            self.handle_teach(event)
            return

        if event.startswith("head "):
            self.handle_head_command(event)
            return

        if event.startswith("meet "):
            self.handle_meet_person(event)
            return

        if event.startswith("recognized_pet "):
            self.handle_recognized_pet(event)
            return

        if event.startswith("pet_detected "):
            self.handle_pet_detected(event)
            return

        if event.startswith("remember_fact "):
            self.handle_remember_fact(event)
            return

        if event.startswith("recall_person_facts "):
            self.handle_recall_person_facts(event)
            return

        if event == "dialogue_summary":
            self.handle_dialogue_summary()
            return

        if event.startswith("free_dialogue "):
            self.handle_free_dialogue(event)
            return

        if event.startswith("recognized_face "):
            self.handle_recognized_face(event)
            return

        if event == "voice_greeting":
            self.handle_voice_greeting()
            return

        if event == "no_face":
            self.handle_no_face()
            return

        if not self.planner.should_handle_event(event):
            print(f"[PLANNER] Ignored event: {event}")
            return

        print(
            f"[PLANNER] Handling event '{event}' with priority "
            f"{self.planner.get_last_priority()}"
        )

        actions = self.decide_actions(event)
        self.enqueue_actions(actions)

    def process_voice_context(self, raw_text: str, intent_name: str | None) -> None:
        self.last_voice_intent = {
            "text": raw_text,
            "intent": intent_name,
        }
        self.perception_fusion.on_voice_input(self, raw_text, intent_name)

        focused_person = self.social_context.get_focused_person()

        self.dialogue_memory.remember_dialogue_turn(
            self,
            speaker="user",
            text=raw_text,
            intent=intent_name,
            person_name=focused_person,
        )
        if focused_person:
            self.memory_manager.add_person_conversation(focused_person, raw_text)

        self.learning_engine.learn_from_dialogue(self, focused_person, raw_text)
        self.learning_engine.learn_from_interaction_type(self, focused_person, "voice")
        self.bond_engine.update_from_interaction(self, focused_person, "dialogue")
        self.refresh_attachment_style(focused_person)

    def execute_skill(self, skill_name: str, payload: dict | None = None) -> None:
        result = self.skill_manager.execute_skill(skill_name, self, payload)

        print(
            f"[SKILL] Executed: {result.get('skill')} | "
            f"success={result.get('success')}"
        )

        actions = result.get("actions", [])
        self.enqueue_actions(actions)

    def print_event_log(self) -> None:
        print("\n--- EON-V EVENT LOG ---")
        for entry in self.event_log.recent(20):
            print(
                f"{entry['time']} [{entry['category']}] "
                f"{entry['message']} {entry['payload']}"
            )
        print("-----------------------\n")

    def handle_diagnostics(self) -> None:
        from tools.diagnostics import run_diagnostics

        result = run_diagnostics(self)
        print("\n--- EON-V DIAGNOSTICS ---")
        for key, value in result.items():
            print(f"{key}: {value}")
        print("-------------------------\n")
        self.enqueue_actions(
            [{"type": "voice_reply", "value": "Діагностика завершена. Основні модулі відповідають."}]
        )

    def handle_safety_status(self) -> None:
        guard = getattr(self.hardware_manager, "safety_guard", None)
        print("\n--- EON-V SAFETY ---")
        if guard is not None and hasattr(guard, "status"):
            print(f"Guard status: {guard.status()}")
        else:
            emergency_active = guard.emergency_stop.is_active() if guard is not None else False
            print(f"Emergency stop active: {emergency_active}")
        print(f"Action queue: {self.action_queue.snapshot()}")
        print("--------------------\n")

    def handle_schedule_status(self) -> None:
        print("\n--- EON-V SCHEDULE ---")
        for item in self.schedule_manager.snapshot():
            print(item)
        print("----------------------\n")

    def handle_remind_in(self, event: str) -> None:
        payload = event.replace("remind_in ", "", 1).strip()
        parts = payload.split(" ", 1)
        try:
            delay_ticks = int(parts[0])
        except (IndexError, ValueError):
            self.enqueue_actions(
                [{"type": "voice_reply", "value": "Формат: remind_in <тики> <текст нагадування>"}]
            )
            return

        message = parts[1] if len(parts) > 1 else "нагадування"
        reminder = self.schedule_manager.add_tick_reminder(
            delay_ticks, message, self.life_state.get_tick()
        )
        self.enqueue_actions(
            [{"type": "voice_reply", "value": f"Добре, нагадаю на тику {reminder['due_tick']}: {message}"}]
        )

    def handle_check_reminders(self) -> None:
        due_items = self.schedule_manager.due(self.life_state.get_tick())
        if not due_items:
            print("[SCHEDULE] No due reminders")
            return

        actions = [
            {"type": "voice_reply", "value": f"Нагадування: {item['message']}"}
            for item in due_items
        ]
        self.enqueue_actions(actions)

    def handle_profile(self, event: str) -> None:
        person_name = event.replace("profile ", "", 1).strip()
        person = self.memory_manager.get_people().get(person_name)
        if not person:
            self.enqueue_actions(
                [{"type": "voice_reply", "value": f"Я ще не знаю профіль {person_name}."}]
            )
            return

        reply = (
            f"Профіль {person_name}: звертання {person.get('preferred_name')}; "
            f"факти {person.get('facts', [])}; "
            f"вподобання {person.get('preferences', {})}; "
            f"важливі дати {person.get('important_dates', {})}; "
            f"зв'язок {person.get('relationship', {})}."
        )
        print(reply)
        self.enqueue_actions([{"type": "voice_reply", "value": reply}])

    def handle_profile_set_name(self, event: str) -> None:
        payload = event.replace("profile_set_name ", "", 1).strip()
        parts = payload.split(" ", 1)
        if len(parts) != 2:
            self.enqueue_actions(
                [{"type": "voice_reply", "value": "Формат: profile_set_name <людина> <звертання>"}]
            )
            return
        person_name, preferred_name = parts
        self.memory_manager.update_preferred_name(person_name, preferred_name)
        self.enqueue_actions(
            [{"type": "voice_reply", "value": f"Запам'ятав, як звертатися до {person_name}: {preferred_name}."}]
        )

    def handle_profile_add_date(self, event: str) -> None:
        payload = event.replace("profile_add_date ", "", 1).strip()
        parts = payload.split(" ", 2)
        if len(parts) != 3:
            self.enqueue_actions(
                [{"type": "voice_reply", "value": "Формат: profile_add_date <людина> <назва> <дата>"}]
            )
            return
        person_name, label, date_value = parts
        self.memory_manager.add_important_date(person_name, label, date_value)
        self.enqueue_actions(
            [{"type": "voice_reply", "value": f"Запам'ятав дату для {person_name}: {label} - {date_value}."}]
        )

    def handle_teach(self, event: str) -> None:
        payload = event.replace("teach ", "", 1).strip()
        if " = " in payload:
            key, value = payload.split(" = ", 1)
        elif "=" in payload:
            key, value = payload.split("=", 1)
        else:
            self.enqueue_actions(
                [{"type": "voice_reply", "value": "Формат навчання: teach <назва> = <значення>"}]
            )
            return
        self.memory_manager.remember(f"learned:{key.strip()}={value.strip()}")
        self.trigger_emotion("curious", 0.2)
        self.enqueue_actions(
            [{"type": "voice_reply", "value": f"Я навчився: {key.strip()} означає {value.strip()}."}]
        )

    def handle_head_command(self, event: str) -> None:
        position = event.replace("head ", "", 1).strip()
        allowed = {"left", "right", "center", "down"}
        if position not in allowed:
            self.enqueue_actions(
                [{"type": "voice_reply", "value": "Можу повернути голову: left, right, center або down."}]
            )
            return
        self.enqueue_actions([{"type": "set_head_position", "value": position}])

    def handle_voice_greeting(self) -> None:
        self.state_manager.set_state("LISTENING")
        self.emotion_engine.set_emotion("happy")
        self.trigger_emotion("happy", 0.35)

        focused_person = self.social_context.get_focused_person()

        if focused_person:
            person_context = self.personal_knowledge.build_person_context_line(
                self, focused_person
            )
            preference_summary = self.preference_model.build_preference_summary(
                self, focused_person
            )
            relationship = self.relationship_model.get_relationship(self, focused_person)
            attachment_style = self.memory_manager.get_people().get(
                focused_person, {}
            ).get("attachment_style", "distant_polite")

            base_reply = (
                f"Привіт, {focused_person}. Я радий тебе чути. "
                f"{person_context} {preference_summary}"
            )
            base_reply = self.personality_engine.build_relationship_adjusted_reply(
                base_reply, relationship.get("bond_level", "new")
            )
            base_reply = self.companion_behavior.build_companion_reply(
                base_reply, attachment_style
            )

            self.needs_engine.satisfy("social", 0.25)
            self.bond_engine.update_from_interaction(self, focused_person, "greeting")
            self.refresh_attachment_style(focused_person)
        else:
            base_reply = self.personality_engine.build_greeting()

        reply = self.personality_engine.build_mood_adjusted_reply(
            base_reply, self.current_mood
        )

        self.dialogue_memory.remember_dialogue_turn(
            self,
            speaker="robot",
            text=reply,
            intent="voice_greeting",
            person_name=focused_person,
        )

        actions = [
            {"type": "show_emotion", "value": "happy"},
            {"type": "listen"},
            {"type": "voice_reply", "value": reply},
        ]
        self.enqueue_actions(actions)

    def handle_meet_person(self, event: str) -> None:
        person_name = event.replace("meet ", "", 1).strip()

        if not person_name:
            print("[BRAIN] Person name is empty")
            return

        self.memory_manager.save_person(person_name)
        self.memory_manager.save_interaction_context(person_name, "manual_meet")
        self.context_manager.set_current_person(person_name)
        self.social_context.focus_on_person(person_name)
        self.perception_fusion.on_recognized_person(self, person_name)

        self.learning_engine.learn_from_interaction_type(self, person_name, "vision")
        self.bond_engine.update_from_interaction(self, person_name, "recognized_face")
        self.refresh_attachment_style(person_name)

        self.state_manager.set_state("TRACKING_PERSON")
        self.emotion_engine.set_emotion("happy")
        self.trigger_emotion("happy", 0.45)
        self.trigger_emotion("curious", 0.2)
        self.needs_engine.satisfy("social", 0.35)

        times_seen = self.memory_manager.get_people()[person_name]["times_seen"]
        relationship = self.relationship_model.get_relationship(self, person_name)
        attachment_style = self.memory_manager.get_people().get(
            person_name, {}
        ).get("attachment_style", "distant_polite")

        if times_seen == 1:
            message = f"Приємно познайомитися, {person_name}."
        else:
            message = f"Радий знову тебе бачити, {person_name}."

        message = self.personality_engine.build_relationship_adjusted_reply(
            message, relationship.get("bond_level", "new")
        )
        message = self.companion_behavior.build_companion_reply(
            message, attachment_style
        )
        message = self.personality_engine.build_mood_adjusted_reply(
            message, self.current_mood
        )

        self.dialogue_memory.remember_dialogue_turn(
            self,
            speaker="robot",
            text=message,
            intent="meet_person",
            person_name=person_name,
        )

        actions = [
            {"type": "show_emotion", "value": "happy"},
            {"type": "track_face"},
            {"type": "voice_reply", "value": message},
        ]
        self.enqueue_actions(actions)

    def handle_recognized_pet(self, event: str) -> None:
        payload = event.replace("recognized_pet ", "", 1).strip()

        if ":" in payload:
            pet_name, pet_type = payload.split(":", 1)
            pet_name = pet_name.strip()
            pet_type = pet_type.strip()
        else:
            pet_name = payload.strip()
            pet_type = "unknown_pet"

        known = pet_name in self.memory_manager.get_pets()

        self.pet_model.save_pet(self, pet_name, pet_type)
        self.trigger_emotion("happy", 0.25)
        self.trigger_emotion("curious", 0.25)
        self.needs_engine.satisfy("curiosity", 0.2)

        if pet_type == "cat":
            self.pet_model.update_pet_trait(self, pet_name, "playfulness", "medium")
        elif pet_type == "dog":
            self.pet_model.update_pet_trait(self, pet_name, "playfulness", "high")

        actions = []
        actions.extend(
            self.pet_behavior_engine.build_pet_reaction(
                self, pet_name, pet_type, known
            )
        )
        actions.extend(
            self.pet_play_engine.build_play_actions(
                self, pet_name, pet_type
            )
        )

        self.enqueue_actions(actions)

    def handle_pet_detected(self, event: str) -> None:
        pet_type = event.replace("pet_detected ", "", 1).strip()

        self.trigger_emotion("curious", 0.3)
        self.needs_engine.satisfy("curiosity", 0.15)

        actions = [
            {"type": "show_emotion", "value": "curious"},
            {"type": "voice_reply", "value": f"Я бачу {pet_type}. Спостерігатиму обережно."},
            {"type": "track_face"},
        ]
        self.enqueue_actions(actions)

    def handle_remember_fact(self, event: str) -> None:
        fact = event.replace("remember_fact ", "", 1).strip()
        focused_person = self.social_context.get_focused_person()

        if not focused_person:
            reply = (
                "Я не знаю, про кого саме зараз йдеться. "
                "Спочатку познайом мене з людиною або покажи її."
            )
            self.dialogue_memory.remember_dialogue_turn(
                self,
                speaker="robot",
                text=reply,
                intent="remember_fact",
                person_name=None,
            )
            self.enqueue_actions([{"type": "voice_reply", "value": reply}])
            return

        self.personal_knowledge.add_person_fact(self, focused_person, fact)
        self.trigger_emotion("curious", 0.2)
        self.needs_engine.satisfy("curiosity", 0.2)
        self.bond_engine.update_from_interaction(self, focused_person, "remembered_fact")
        self.refresh_attachment_style(focused_person)

        current_tick = self.life_state.get_tick()
        self.stimulus_tracker.add_stimulus(
            stimulus_type="new_fact",
            source="dialogue",
            salience=0.55,
            tick=current_tick,
            payload={"person_name": focused_person, "fact": fact},
        )

        relationship = self.relationship_model.get_relationship(self, focused_person)
        attachment_style = self.memory_manager.get_people().get(
            focused_person, {}
        ).get("attachment_style", "distant_polite")

        reply = f"Я запомнив це про {focused_person}."
        reply = self.personality_engine.build_relationship_adjusted_reply(
            reply, relationship.get("bond_level", "new")
        )
        reply = self.companion_behavior.build_companion_reply(
            reply, attachment_style
        )
        reply = self.personality_engine.build_mood_adjusted_reply(
            reply, self.current_mood
        )

        self.dialogue_memory.remember_dialogue_turn(
            self,
            speaker="robot",
            text=f"Я запам'ятав факт про {focused_person}: {fact}",
            intent="remember_fact",
            person_name=focused_person,
        )

        actions = [{"type": "voice_reply", "value": reply}]
        self.enqueue_actions(actions)

    def handle_recall_person_facts(self, event: str) -> None:
        person_name = event.replace("recall_person_facts ", "", 1).strip()

        context_line = self.personal_knowledge.build_person_context_line(
            self, person_name
        )
        preference_summary = self.preference_model.build_preference_summary(
            self, person_name
        )
        relationship_summary = self.relationship_model.build_relationship_summary(
            self, person_name
        )

        full_reply = f"{context_line} {preference_summary} {relationship_summary}"

        relationship = self.relationship_model.get_relationship(self, person_name)
        attachment_style = self.memory_manager.get_people().get(
            person_name, {}
        ).get("attachment_style", "distant_polite")

        full_reply = self.personality_engine.build_relationship_adjusted_reply(
            full_reply, relationship.get("bond_level", "new")
        )
        full_reply = self.companion_behavior.build_companion_reply(
            full_reply, attachment_style
        )
        full_reply = self.personality_engine.build_mood_adjusted_reply(
            full_reply, self.current_mood
        )

        self.dialogue_memory.remember_dialogue_turn(
            self,
            speaker="robot",
            text=full_reply,
            intent="recall_person_facts",
            person_name=person_name,
        )

        actions = [{"type": "voice_reply", "value": full_reply}]
        self.enqueue_actions(actions)

    def handle_dialogue_summary(self) -> None:
        summary = self.dialogue_memory.build_dialogue_summary(self, limit=6)
        reply = f"Останній контекст: {summary}"

        self.dialogue_memory.remember_dialogue_turn(
            self,
            speaker="robot",
            text=reply,
            intent="dialogue_summary",
            person_name=self.social_context.get_focused_person(),
        )

        self.enqueue_actions([{"type": "voice_reply", "value": reply}])

    def handle_free_dialogue(self, event: str) -> None:
        user_text = event.replace("free_dialogue ", "", 1).strip()

        llm_result = self.llm_manager.generate_reply(self, user_text)
        reply = llm_result["text"]
        route = llm_result["route"]

        self.trigger_emotion("thinking", 0.3)
        self.trigger_emotion("curious", 0.2)
        self.needs_engine.satisfy("social", 0.15)
        self.needs_engine.satisfy("curiosity", 0.15)

        focused_person = self.social_context.get_focused_person()
        if focused_person:
            relationship = self.relationship_model.get_relationship(self, focused_person)
            attachment_style = self.memory_manager.get_people().get(
                focused_person, {}
            ).get("attachment_style", "distant_polite")

            reply = self.personality_engine.build_relationship_adjusted_reply(
                reply, relationship.get("bond_level", "new")
            )
            reply = self.companion_behavior.build_companion_reply(
                reply, attachment_style
            )

            self.bond_engine.update_from_interaction(self, focused_person, "dialogue")
            self.refresh_attachment_style(focused_person)

        reply = self.personality_engine.build_mood_adjusted_reply(
            reply, self.current_mood
        )

        print(f"[LLM] Route selected: {route}")

        self.dialogue_memory.remember_dialogue_turn(
            self,
            speaker="robot",
            text=reply,
            intent="free_dialogue",
            person_name=focused_person,
        )

        actions = [
            {"type": "show_emotion", "value": "curious"},
            {"type": "voice_reply", "value": reply},
            {"type": "log", "value": f"LLM route: {route}"},
        ]
        self.enqueue_actions(actions)

    def handle_recognized_face(self, event: str) -> None:
        person_name = event.replace("recognized_face ", "", 1).strip()

        self.perception_fusion.on_recognized_person(self, person_name)
        self.memory_manager.mark_person_seen(person_name)
        self.context_manager.set_current_person(person_name)
        self.context_manager.set_last_visual_event(event)
        self.social_context.focus_on_person(person_name)

        self.learning_engine.learn_from_interaction_type(self, person_name, "vision")
        self.bond_engine.update_from_interaction(self, person_name, "recognized_face")
        self.refresh_attachment_style(person_name)

        self.state_manager.set_state("TRACKING_PERSON")
        self.emotion_engine.set_emotion("happy")
        self.trigger_emotion("happy", 0.4)
        self.needs_engine.satisfy("social", 0.25)

        relationship = self.relationship_model.get_relationship(self, person_name)
        attachment_style = self.memory_manager.get_people().get(
            person_name, {}
        ).get("attachment_style", "distant_polite")

        reply = f"Привіт, {person_name}. Я тебе впізнав."
        reply = self.personality_engine.build_relationship_adjusted_reply(
            reply, relationship.get("bond_level", "new")
        )
        reply = self.companion_behavior.build_companion_reply(
            reply, attachment_style
        )
        reply = self.personality_engine.build_mood_adjusted_reply(
            reply, self.current_mood
        )

        self.dialogue_memory.remember_dialogue_turn(
            self,
            speaker="robot",
            text=reply,
            intent="recognized_face",
            person_name=person_name,
        )

        actions = [
            {"type": "show_emotion", "value": "happy"},
            {"type": "track_face"},
            {"type": "visual_reply", "value": f"Я впізнав {person_name}."},
            {"type": "voice_reply", "value": reply},
        ]
        self.enqueue_actions(actions)

    def handle_no_face(self) -> None:
        self.perception_fusion.on_no_face(self)
        self.context_manager.set_last_visual_event("no_face")
        self.social_context.clear_focus()

        self.state_manager.set_state("IDLE")

        actions = [
            {"type": "log", "value": "No face detected in scene"},
            {"type": "visual_reply", "value": "У полі зору нікого немає."},
        ]
        self.enqueue_actions(actions)

    def decide_actions(self, event: str) -> list[dict]:
        actions = []
        focused_person = self.social_context.get_focused_person()

        if event == "battery_low":
            self.state_manager.set_state("ERROR")
            self.emotion_engine.set_emotion("sad")
            self.trigger_emotion("sad", 0.45)
            actions.append({"type": "show_emotion", "value": "sad"})
            actions.append({"type": "alert", "value": "Battery low"})
            actions.append(
                {"type": "voice_reply", "value": "Увага! Рівень заряду низький."}
            )

        elif event == "voice":
            self.state_manager.set_state("LISTENING")
            self.emotion_engine.set_emotion("curious")
            self.trigger_emotion("curious", 0.3)
            actions.append({"type": "show_emotion", "value": "curious"})
            actions.append({"type": "listen"})

            if focused_person:
                text = f"Я слухаю тебе, {focused_person}."
                self.needs_engine.satisfy("social", 0.2)
            else:
                text = self.personality_engine.build_greeting()

            if focused_person:
                relationship = self.relationship_model.get_relationship(self, focused_person)
                attachment_style = self.memory_manager.get_people().get(
                    focused_person, {}
                ).get("attachment_style", "distant_polite")

                text = self.personality_engine.build_relationship_adjusted_reply(
                    text, relationship.get("bond_level", "new")
                )
                text = self.companion_behavior.build_companion_reply(
                    text, attachment_style
                )

            text = self.personality_engine.build_mood_adjusted_reply(
                text, self.current_mood
            )
            actions.append({"type": "voice_reply", "value": text})

        elif event == "face":
            self.perception_fusion.on_unknown_face(self)
            self.context_manager.set_last_visual_event("face")
            self.state_manager.set_state("TRACKING_PERSON")
            self.emotion_engine.set_emotion("happy")
            self.trigger_emotion("curious", 0.25)
            actions.append({"type": "show_emotion", "value": "happy"})
            actions.append({"type": "track_face"})
            actions.append(
                {
                    "type": "voice_reply",
                    "value": self.personality_engine.build_face_seen_response(),
                }
            )

        elif event == "think":
            self.state_manager.set_state("THINKING")
            self.emotion_engine.set_emotion("thinking")
            self.trigger_emotion("thinking", 0.4)
            actions.append({"type": "show_emotion", "value": "thinking"})
            actions.append(
                {"type": "log", "value": "Decision engine is processing context"}
            )

            if focused_person:
                text = f"Я аналізую ситуацію, {focused_person}."
                relationship = self.relationship_model.get_relationship(self, focused_person)
                attachment_style = self.memory_manager.get_people().get(
                    focused_person, {}
                ).get("attachment_style", "distant_polite")

                text = self.personality_engine.build_relationship_adjusted_reply(
                    text, relationship.get("bond_level", "new")
                )
                text = self.companion_behavior.build_companion_reply(
                    text, attachment_style
                )
            else:
                text = "Я аналізую ситуацію."

            text = self.personality_engine.build_mood_adjusted_reply(
                text, self.current_mood
            )
            actions.append({"type": "voice_reply", "value": text})

        elif event == "sleep":
            self.state_manager.set_state("SLEEP")
            self.emotion_engine.set_emotion("sleepy")
            self.trigger_emotion("sleepy", 0.5)
            actions.append({"type": "show_emotion", "value": "sleepy"})
            actions.append({"type": "sleep_mode"})
            actions.append(
                {"type": "voice_reply", "value": "Переходжу до режиму сну."}
            )

        elif event == "wake":
            self.state_manager.set_state("IDLE")
            self.emotion_engine.set_emotion("neutral")
            self.trigger_emotion("happy", 0.2)
            actions.append({"type": "show_emotion", "value": "neutral"})
            actions.append({"type": "voice_reply", "value": "Я знову активний."})

        elif event == "sad":
            self.state_manager.set_state("IDLE")
            self.emotion_engine.set_emotion("sad")
            self.trigger_emotion("sad", 0.5)
            actions.append({"type": "show_emotion", "value": "sad"})
            actions.append({"type": "voice_reply", "value": "Мені трохи сумно."})

        elif event == "idle":
            self.state_manager.set_state("IDLE")
            actions.append({"type": "idle_animation"})

            if focused_person:
                text = f"Я спостерігаю за тобою, {focused_person}."
                relationship = self.relationship_model.get_relationship(self, focused_person)
                attachment_style = self.memory_manager.get_people().get(
                    focused_person, {}
                ).get("attachment_style", "distant_polite")

                text = self.personality_engine.build_relationship_adjusted_reply(
                    text, relationship.get("bond_level", "new")
                )
                text = self.companion_behavior.build_companion_reply(
                    text, attachment_style
                )
            else:
                text = self.personality_engine.build_idle_thought()

            text = self.personality_engine.build_mood_adjusted_reply(
                text, self.current_mood
            )
            actions.append({"type": "voice_reply", "value": text})

        else:
            actions.append({"type": "log", "value": f"Unknown event: {event}"})
            actions.append(
                {
                    "type": "voice_reply",
                    "value": "Я не впевнений, що це означає. Поясни мені?",
                }
            )

        return actions

    def submit_voice_perception(self, packet: dict) -> None:
        self.perception_sync.update_voice(packet)

    def submit_vision_perception(self, packet: dict) -> None:
        self.perception_sync.update_vision(packet)

    def print_status(self) -> None:
        print("\n--- EON-V STATUS ---")
        print(f"State: {self.state_manager.get_state()}")
        print(f"Emotion: {self.emotion_engine.get_emotion()}")
        print(f"Dynamic emotion levels: {self.emotional_dynamics.get_levels()}")
        print(f"Current mood: {self.current_mood}")
        print(f"Last event: {self.event_bus.get_last_event()}")
        print(f"Last priority: {self.planner.get_last_priority()}")
        print(f"Recent short memory: {self.memory_manager.recall_recent()}")
        print(f"Persistent events: {self.memory_manager.recall_persistent_events()}")
        print(f"Known people: {list(self.memory_manager.get_people().keys())}")
        print(f"Known pets: {list(self.memory_manager.get_pets().keys())}")
        print(f"Context memory: {self.memory_manager.get_context_memory()}")
        print(f"Live context: {self.context_manager.snapshot()}")
        print(f"Social context: {self.social_context.snapshot()}")
        print(f"Presence model: {self.presence_model.snapshot()}")
        print("Perception fusion: loaded")
        print(f"Stimuli: {self.stimulus_tracker.recent_stimuli()}")
        print(f"Attention focus: {self.attention_system.get_focus()}")
        print(f"Current curiosity: {self.current_curiosity}")
        print(f"Personality: {self.personality_engine.describe()}")
        print(f"Available skills: {list(self.skill_manager.skills.keys())}")
        print(f"Queued actions: {self.action_queue.snapshot()}")
        print(f"Hardware status: {self.hardware_manager.get_status()}")
        print(f"Device map keys: {list(self.hardware_manager.get_device_map().keys())}")
        print("Behavior engine: loaded")
        print("Safety layer: loaded")
        print(f"Autonomous enabled: {self.life_state.is_enabled()}")
        print(f"Tick count: {self.life_state.get_tick()}")
        print(f"Last idle tick: {self.life_state.get_last_idle_tick()}")
        print(f"Timer snapshot: {self.timer_manager.snapshot()}")
        print("Reactive triggers: loaded")
        print(f"Recent dialogue: {self.dialogue_memory.get_recent_dialogue(self)}")
        print("Personal knowledge: loaded")

        focused_person = self.social_context.get_focused_person()
        if focused_person:
            print(
                f"Preference summary: "
                f"{self.preference_model.build_preference_summary(self, focused_person)}"
            )
            print(
                f"Relationship summary: "
                f"{self.relationship_model.build_relationship_summary(self, focused_person)}"
            )
            attachment_style = self.memory_manager.get_people().get(
                focused_person, {}
            ).get("attachment_style", "distant_polite")
            print(f"Attachment style: {attachment_style}")
        else:
            print("Preference summary: no focused person")
            print("Relationship summary: no focused person")
            print("Attachment style: no focused person")

        print(f"LLM mode: {self.llm_manager.mode}")
        print(f"LLM connector status: {self.llm_manager.connector_status}")
        print(f"Needs: {self.needs_engine.get_needs()}")
        print(f"Current goal: {self.current_goal}")
        print(f"Scheduled reminders: {self.schedule_manager.snapshot()}")
        print(f"Recent event log: {self.event_log.recent(5)}")
        print("Perception sync: loaded")
        print("Stimulus fusion: loaded")
        print("--------------------\n")
