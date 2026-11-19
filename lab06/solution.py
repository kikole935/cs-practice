from pathlib import Path

def count_by_extension(paths: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for path in paths:
        ext = Path(path).suffix.lstrip(".").lower()
        counts[ext] = counts.get(ext, 0) + 1
    return counts

def deepest_path(paths: list[str]) -> str:
    if not paths:
        return ""
    return min(paths, key=lambda p: (-p.count("/"), p))
def human_size(n_bytes: int) -> str:
    if n_bytes < 1024:
        return f"{n_bytes} Б"
    size = float(n_bytes)
    for unit in ("Б", "КБ", "МБ", "ГБ", "ТБ"):
        if size < 1024 or unit == "ТБ":
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} ТБ"
