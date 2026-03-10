from __future__ import annotations

from bs4 import BeautifulSoup


def parse_sigaa_class_status(html: str) -> dict[str, int | str | None]:
    """Parse class seat status from SIGAA HTML.

    IMPORTANT:
    This parser uses generic/fictitious selectors as placeholders.
    You MUST inspect the real SIGAA page and adjust selectors accordingly.
    """
    soup = BeautifulSoup(html, "html.parser")

    # --- Adapt the selectors below to SIGAA real structure ---
    total_seats_text = _get_text(soup, "#total-vagas")
    occupied_seats_text = _get_text(soup, "#vagas-ocupadas")
    available_seats_text = _get_text(soup, "#vagas-disponiveis")
    status_text = _get_text(soup, ".status-turma")

    return {
        "total_seats": _to_int(total_seats_text),
        "occupied_seats": _to_int(occupied_seats_text),
        "available_seats": _to_int(available_seats_text),
        "status": status_text,
    }



def _get_text(soup: BeautifulSoup, selector: str) -> str | None:
    element = soup.select_one(selector)
    if not element:
        return None
    text = element.get_text(strip=True)
    return text or None



def _to_int(value: str | None) -> int | None:
    if value is None:
        return None
    digits = "".join(ch for ch in value if ch.isdigit())
    if not digits:
        return None
    return int(digits)
