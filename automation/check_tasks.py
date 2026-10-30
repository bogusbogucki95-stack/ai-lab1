#!/usr/bin/env python3
"""Checks repository sample tasks. Does not access browser localStorage."""
import json
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
source = ROOT / "tasks.example.json"
data = json.loads(source.read_text(encoding="utf-8"))
today = date.today()
lines = ["# AI LAB — raport zadań", "", f"Data kontroli: {today.isoformat()}", ""]
for task in data.get("tasks", []):
    if task.get("done"):
        status = "ukończone"
    else:
        try:
            days = (date.fromisoformat(task["due"]) - today).days
            status = "po terminie" if days < 0 else ("do 7 dni" if days <= 7 else "zaplanowane")
        except (KeyError, ValueError, TypeError):
            status = "bez terminu"
    lines.append(f"- {task.get('name', 'Bez nazwy')} — {status}")
report = "\n".join(lines) + "\n"
output = ROOT / "report.md"
output.write_text(report, encoding="utf-8")
print(report)
