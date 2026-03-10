from __future__ import annotations

import unittest
from pathlib import Path

from parser import parse_sigaa_class_status


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _load_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text(encoding="utf-8")


class ParseSigaaClassStatusTests(unittest.TestCase):
    def test_parse_with_primary_selectors(self) -> None:
        html = _load_fixture("sigaa_class_primary_selectors.html")

        parsed = parse_sigaa_class_status(html)

        self.assertEqual(parsed["total_seats"], 40)
        self.assertEqual(parsed["occupied_seats"], 30)
        self.assertEqual(parsed["available_seats"], 10)
        self.assertEqual(parsed["status"], "ABERTA")

    def test_parse_fallback_with_regex(self) -> None:
        html = _load_fixture("sigaa_class_fallback_regex.html")

        parsed = parse_sigaa_class_status(html)

        self.assertEqual(parsed["total_seats"], 60)
        self.assertEqual(parsed["occupied_seats"], 58)
        self.assertEqual(parsed["available_seats"], 2)
        self.assertEqual(parsed["status"], "AGUARDANDO CONFIRMAÇÃO")

    def test_raises_when_fields_are_missing(self) -> None:
        html = _load_fixture("sigaa_class_missing_fields.html")

        with self.assertRaisesRegex(ValueError, "campos obrigatórios"):
            parse_sigaa_class_status(html)

    def test_raises_when_values_are_inconsistent(self) -> None:
        html = _load_fixture("sigaa_class_invalid_inconsistent.html")

        with self.assertRaisesRegex(ValueError, "available_seats"):
            parse_sigaa_class_status(html)


if __name__ == "__main__":
    unittest.main()
