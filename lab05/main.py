from pathlib import Path

from logstats import count_levels, format_report, top_errors

def main() -> None:
    filename = input().strip()
    base_dir = Path(__file__).resolve().parent

    log_path = Path(filename)
    if not log_path.exists():
        candidate = base_dir / filename
        if candidate.exists():
            log_path = candidate

    with open(log_path, encoding="utf-8") as log_file:
        counts = count_levels(log_file)

    with open(log_path, encoding="utf-8") as log_file:
        errors = top_errors(log_file, 3)

    total_parsed = sum(counts.values())
    print(total_parsed)
    print(counts.get("ERROR", 0))
    print(counts.get("BROKEN", 0))

    report_text = format_report(counts, errors)
    report_path = base_dir / "report.txt"
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write(report_text)

if __name__ == "__main__":
    main()
