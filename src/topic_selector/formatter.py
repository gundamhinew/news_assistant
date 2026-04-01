from __future__ import annotations

from .models import Candidate


def _to_cn_title(raw: str) -> str:
    cleaned = raw.replace(";", "，").replace(":", "，").replace("-", "，")
    if "，" not in cleaned:
        cleaned = f"{cleaned}，关注后续影响"
    parts = [p.strip() for p in cleaned.split("，") if p.strip()]
    if len(parts) == 1:
        parts.append("关注后续影响")
    return f"{parts[0]}，{parts[1]}"


def render_list(candidates: list[Candidate]) -> str:
    lines: list[str] = []
    for i, c in enumerate(candidates, start=1):
        d = c.article.published_at
        date_s = f"{d.year}-{d.month}-{d.day}"
        title = _to_cn_title(c.article.title)
        lines.append(f"{i}.【{c.primary_label}】{title}（{c.article.source_name_zh} {date_s}）")
        lines.append(c.article.url)
    return "\n".join(lines)
