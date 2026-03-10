from __future__ import annotations

import re
from collections.abc import Iterable

from bs4 import BeautifulSoup


FIELD_SELECTORS: dict[str, tuple[str, ...]] = {
    "total_seats": (
        "#form\:turma [id$='qtdVagasOfertadas']",
        "#form\:turma [id$='vagasOfertadas']",
        "table.formulario td:has(+ td span[id$='qtdVagasOfertadas']) + td",
    ),
    "occupied_seats": (
        "#form\:turma [id$='qtdVagasOcupadas']",
        "#form\:turma [id$='vagasOcupadas']",
        "table.formulario td:has(+ td span[id$='qtdVagasOcupadas']) + td",
    ),
    "available_seats": (
        "#form\:turma [id$='qtdVagasDisponiveis']",
        "#form\:turma [id$='vagasDisponiveis']",
        "table.formulario td:has(+ td span[id$='qtdVagasDisponiveis']) + td",
    ),
    "status": (
        "#form\:turma [id$='situacaoTurma']",
        "#form\:turma [id$='situacao']",
        "table.formulario td:has(+ td span[id$='situacaoTurma']) + td",
    ),
}

FIELD_REGEX: dict[str, re.Pattern[str]] = {
    "total_seats": re.compile(r"vagas\s+ofertadas?\s*[:\-]?\s*(\d+)", re.IGNORECASE),
    "occupied_seats": re.compile(r"vagas\s+ocupadas?\s*[:\-]?\s*(\d+)", re.IGNORECASE),
    "available_seats": re.compile(r"vagas\s+dispon[ií]veis\s*[:\-]?\s*(\d+)", re.IGNORECASE),
    "status": re.compile(r"situa[cç][aã]o\s*[:\-]?\s*([\w\s\-/]+)", re.IGNORECASE),
}



def parse_sigaa_class_status(html: str) -> dict[str, int | str | None]:
    """Parse class seat status from SIGAA class query HTML."""
    soup = BeautifulSoup(html, "html.parser")

    parsed = {
        "total_seats": _extract_number(soup, html, "total_seats"),
        "occupied_seats": _extract_number(soup, html, "occupied_seats"),
        "available_seats": _extract_number(soup, html, "available_seats"),
        "status": _extract_text(soup, html, "status"),
    }

    _validate_parsed_result(parsed)
    return parsed



def _extract_number(soup: BeautifulSoup, html: str, field: str) -> int | None:
    text = _extract_text(soup, html, field)
    return _to_int(text)



def _extract_text(soup: BeautifulSoup, html: str, field: str) -> str | None:
    selector_value = _extract_by_selectors(soup, FIELD_SELECTORS[field])
    if selector_value is not None:
        return selector_value
    return _extract_by_regex(html, FIELD_REGEX[field])



def _extract_by_selectors(soup: BeautifulSoup, selectors: Iterable[str]) -> str | None:
    for selector in selectors:
        element = soup.select_one(selector)
        if not element:
            continue
        text = element.get_text(" ", strip=True)
        if text:
            return text
    return None



def _extract_by_regex(html: str, pattern: re.Pattern[str]) -> str | None:
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    match = pattern.search(text)
    if not match:
        return None
    return match.group(1).strip()



def _to_int(value: str | None) -> int | None:
    if value is None:
        return None
    digits = "".join(ch for ch in value if ch.isdigit())
    if not digits:
        return None
    return int(digits)



def _validate_parsed_result(parsed: dict[str, int | str | None]) -> None:
    missing_fields = [field for field in ("total_seats", "occupied_seats", "available_seats") if parsed[field] is None]
    if missing_fields:
        raise ValueError(
            "Não foi possível identificar campos obrigatórios na página SIGAA: "
            f"{', '.join(missing_fields)}."
        )

    total = parsed["total_seats"]
    occupied = parsed["occupied_seats"]
    available = parsed["available_seats"]

    if not isinstance(total, int) or not isinstance(occupied, int) or not isinstance(available, int):
        raise ValueError("Campos de vagas retornaram em formato inválido.")

    if available > total:
        raise ValueError(f"Inconsistência nos dados SIGAA: available_seats ({available}) > total_seats ({total}).")

    if occupied > total:
        raise ValueError(f"Inconsistência nos dados SIGAA: occupied_seats ({occupied}) > total_seats ({total}).")

    if occupied + available != total:
        raise ValueError(
            "Inconsistência nos dados SIGAA: occupied_seats + available_seats "
            f"({occupied} + {available}) != total_seats ({total})."
        )
