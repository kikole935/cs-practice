from collections.abc import Iterable

VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR"}

def parse_event(line: str) -> dict:
    stripped = line.strip()
    if not stripped:
        raise ValueError("Пустая строка журнала")

    parts = stripped.split(maxsplit=2)
    if len(parts) < 3:
        raise ValueError(f"Некорректный формат строки: {line!r}")

    time_str, level, message = parts
    if not time_str or level not in VALID_LEVELS or not message:
        raise ValueError(f"Некорректный уровень или пустое поле: {line!r}")

    return {
        "time": time_str,
        "level": level,
        "message": message,
    }

def count_levels(lines: Iterable[str]) -> dict:
    counts = {
        "BROKEN": 0,
        "DEBUG": 0,
        "ERROR": 0,
        "INFO": 0,
        "WARNING": 0,
    }

    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line)
        except ValueError:
            counts["BROKEN"] += 1
        else:
            counts[event["level"]] += 1

    return counts

def top_errors(lines: Iterable[str], n: int = 3) -> list[list]:
    error_counts: dict[str, int] = {}

    for line in lines:
        if not line.strip():
            continue
        try:
            event = parse_event(line)
        except ValueError:
            continue

        if event["level"] == "ERROR":
            msg = event["message"]
            error_counts[msg] = error_counts.get(msg, 0) + 1

    sorted_errors = sorted(
        error_counts.items(),
        key=lambda item: (-item[1], item[0]),
    )
    return [[msg, count] for msg, count in sorted_errors[:n]]

def format_report(counts: dict, errors: list[list]) -> str:
    report_lines = ["Отчёт по журналу", ""]

    for level in sorted(counts):
        report_lines.append(f"{level}: {counts[level]}")

    report_lines.append("")
    report_lines.append("Частые ошибки:")

    for message, count in errors:
        report_lines.append(f"- {message} — {count}")

    return "\n".join(report_lines) + "\n"
