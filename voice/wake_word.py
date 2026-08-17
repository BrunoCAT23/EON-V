from __future__ import annotations

import re
from dataclasses import dataclass

from settings import WAKE_WORD_FUZZY, WAKE_WORD_MAX_DISTANCE, WAKE_WORDS


@dataclass(frozen=True)
class WakeMatch:
    detected: bool
    start: int = 0
    end: int = 0
    word: str = ""


class WakeWordDetector:
    def __init__(self, wake_words: list[str] | None = None) -> None:
        configured_words = wake_words or [word.strip() for word in WAKE_WORDS.split(",")]
        self.wake_words = [word.lower() for word in configured_words if word.strip()]
        self.compact_wake_words = {self._compact(word) for word in self.wake_words}

    def detect(self, text: str) -> bool:
        return self.find(text).detected

    def find(self, text: str) -> WakeMatch:
        normalized = self._normalize(text)
        if not normalized:
            return WakeMatch(False)

        direct = self._find_direct(normalized)
        if direct.detected:
            return direct

        if not WAKE_WORD_FUZZY:
            return WakeMatch(False)

        return self._find_fuzzy_at_start(normalized)

    def remove_wake_word(self, text: str) -> str:
        normalized = self._normalize(text)
        match = self.find(normalized)

        if match.detected:
            return (normalized[: match.start] + normalized[match.end :]).strip(" ,.!?-")

        cleaned = normalized
        for word in self.wake_words:
            cleaned = re.sub(rf"\b{re.escape(word)}\b", "", cleaned).strip(" ,.!?-")

        return cleaned.strip()

    def _find_direct(self, text: str) -> WakeMatch:
        for word in sorted(self.wake_words, key=len, reverse=True):
            pattern = rf"(^|[\s,.!?\-])({re.escape(word)})($|[\s,.!?\-])"
            match = re.search(pattern, text)
            if match:
                return WakeMatch(True, match.start(2), match.end(2), word)

        compact_text = self._compact(text)
        for word in sorted(self.compact_wake_words, key=len, reverse=True):
            if word and compact_text.startswith(word):
                return WakeMatch(True, 0, min(len(text), len(word)), word)

        return WakeMatch(False)

    def _find_fuzzy_at_start(self, text: str) -> WakeMatch:
        words = re.findall(r"[\wа-яіїєґ']+", text, flags=re.IGNORECASE)
        if not words:
            return WakeMatch(False)

        candidates = [words[0]]
        if len(words) >= 2:
            candidates.append(words[0] + words[1])

        first_pos = text.find(words[0])
        for candidate in candidates:
            compact_candidate = self._compact(candidate)
            for wake_word in self.compact_wake_words:
                if not wake_word:
                    continue
                if self._distance(compact_candidate[: len(wake_word)], wake_word) <= WAKE_WORD_MAX_DISTANCE:
                    end = first_pos + len(words[0])
                    if len(candidate) > len(words[0]) and len(words) >= 2:
                        second_pos = text.find(words[1], end)
                        if second_pos >= 0:
                            end = second_pos + len(words[1])
                    return WakeMatch(True, first_pos, end, wake_word)

        return WakeMatch(False)

    def _normalize(self, text: str) -> str:
        return re.sub(r"\s+", " ", text.strip().lower())

    def _compact(self, text: str) -> str:
        substitutions = {
            "ё": "е",
            "є": "е",
            "і": "и",
            "ї": "и",
            "й": "и",
            "о": "o",
            "е": "e",
            "н": "n",
            "в": "v",
        }
        normalized = self._normalize(text)
        normalized = "".join(substitutions.get(char, char) for char in normalized)
        return re.sub(r"[^a-z0-9а-яіїєґ]", "", normalized)

    def _distance(self, left: str, right: str) -> int:
        if left == right:
            return 0
        if abs(len(left) - len(right)) > WAKE_WORD_MAX_DISTANCE:
            return WAKE_WORD_MAX_DISTANCE + 1

        previous = list(range(len(right) + 1))
        for index_left, char_left in enumerate(left, start=1):
            current = [index_left]
            for index_right, char_right in enumerate(right, start=1):
                cost = 0 if char_left == char_right else 1
                current.append(
                    min(
                        previous[index_right] + 1,
                        current[index_right - 1] + 1,
                        previous[index_right - 1] + cost,
                    )
                )
            previous = current

        return previous[-1]
