import os
import unittest

os.environ["WAKE_WORD_FUZZY"] = "true"

from voice.wake_word import WakeWordDetector


class WakeWordDetectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = WakeWordDetector()

    def test_detects_common_eon_variants(self) -> None:
        for phrase in [
            "eon привіт",
            "EON статус",
            "еон прокинься",
            "йон привіт",
            "іон статус",
            "e on привіт",
        ]:
            with self.subTest(phrase=phrase):
                self.assertTrue(self.detector.detect(phrase))

    def test_removes_wake_word_variant(self) -> None:
        self.assertEqual(self.detector.remove_wake_word("йон привіт"), "привіт")

    def test_does_not_trigger_on_random_sentence(self) -> None:
        self.assertFalse(self.detector.detect("привіт як справи"))


if __name__ == "__main__":
    unittest.main()
