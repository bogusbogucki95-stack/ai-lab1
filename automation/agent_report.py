"""AI LAB 2.8: deterministic task report; no LLM, no external calls."""
import datetime
import os
from pathlib import Path

task = os.environ.get("AI_LAB_TASK", "").strip()[:500]
category = os.environ.get("AI_LAB_CATEGORY", "checklist")
if not task:
    raise SystemExit("Task cannot be empty")
templates = {
    "checklist": [
        "Zdefiniuj mierzalny rezultat i termin.",
        "Zidentyfikuj wymagane dane oraz źródła.",
        "Podziel pracę na trzy małe kroki.",
        "Weryfikuj wynik przed wdrożeniem.",
    ],
    "risk": [
        "Spisz założenia i zależności.",
        "Oceń ryzyko finansowe, prawne i operacyjne.",
        "Zaplanuj wariant awaryjny.",
        "Ustal warunek zatrzymania eksperymentu.",
    ],
    "ecommerce": [
        "Sprawdź popyt i grupę docelową.",
        "Policz marżę po VAT, dostawie, zwrotach i reklamie.",
        "Zweryfikuj dostawcę oraz dostępność towaru.",
        "Uruchom mały test sprzedaży i zmierz konwersję.",
    ],
}
if category not in templates:
    raise SystemExit("Unsupported category")
lines = [
    "# AI LAB 2.8 — raport roboczy",
    "",
    f"Data UTC: {datetime.datetime.now(datetime.timezone.utc).isoformat()}",
    f"Zadanie: {task.replace(chr(10), ' ')}",
    f"Szablon: {category}",
    "",
    "## Lista działań",
]
lines.extend(f"{i}. {item}" for i, item in enumerate(templates[category], 1))
lines += [
    "",
    "## Ograniczenia",
    "Raport jest generowany regułowo, bez modelu AI i bez sprawdzania faktów.",
    "Nie stanowi wykonania opisanego zadania ani analizy danych rynkowych.",
]
path = Path("reports/agent-report.md")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Report generated:", path)
