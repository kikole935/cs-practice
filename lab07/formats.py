from __future__ import annotations

import json
import math

def _parse_scalar(raw: str) -> int | float | bool | str:
    value = raw.strip()
    lower = value.lower()

    if lower in ("true", "yes"):
        return True
    if lower in ("false", "no"):
        return False

    try:
        return int(value)
    except ValueError:
        pass

    try:
        num = float(value)
        if math.isfinite(num):
            return num
    except ValueError:
        pass

    return value

def csv_to_records(text: str) -> list[dict]:
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) < 2:
        return []

    headers = lines[0].split(",")
    records: list[dict] = []

    for line in lines[1:]:
        values = line.split(",")
        record = {
            headers[i]: (values[i] if i < len(values) else "")
            for i in range(len(headers))
        }
        records.append(record)

    return records

def parse_settings(lines: list[str]) -> dict:
    settings: dict = {}
    current_list_key: str | None = None

    for raw_line in lines:
        cleaned = raw_line.split("#", 1)[0].strip()
        if not cleaned:
            continue

        if cleaned.startswith("- ") or cleaned == "-":
            if current_list_key is not None:
                item_raw = cleaned[2:].strip() if cleaned.startswith("- ") else ""
                settings[current_list_key].append(_parse_scalar(item_raw))
            continue

        key_part, sep, val_part = cleaned.partition(":")
        if not sep:
            continue

        key = key_part.strip()
        val = val_part.strip()

        if val == "":
            settings[key] = []
            current_list_key = key
        else:
            settings[key] = _parse_scalar(val)
            current_list_key = None

    return settings

def merge_by_key(rows: list[dict], extra: dict, key: str = "id") -> list[dict]:
    result: list[dict] = []

    for row in rows:
        lookup = row.get(key)
        extra_info = None

        if lookup in extra:
            extra_info = extra[lookup]
        elif lookup is not None and str(lookup) in extra:
            extra_info = extra[str(lookup)]

        if isinstance(extra_info, dict):
            result.append({**extra_info, **row})
        else:
            result.append(dict(row))

    return result

def records_to_json(records: list[dict]) -> str:
    return json.dumps(records, ensure_ascii=False, indent=2, sort_keys=True)
