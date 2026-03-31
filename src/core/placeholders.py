from __future__ import annotations

from dataclasses import dataclass

# ======= 顶部占位符 =======
ISSUE_NO = "{{ISSUE_NO}}"
DATE_Y = "{{DATE_Y}}"
DATE_M = "{{DATE_M}}"
DATE_D = "{{DATE_D}}"


@dataclass(frozen=True)
class NewsPlaceholders:
    topic: str
    title: str
    media: str
    date_y: str
    date_m: str
    date_d: str
    body: str


def news_placeholders(i: int) -> NewsPlaceholders:
    """
    i: 1..10
    """
    if not (1 <= i <= 10):
        raise ValueError(f"news index out of range: {i}")

    return NewsPlaceholders(
        topic=f"{{{{N{i}_TOPIC}}}}",
        title=f"{{{{N{i}_TITLE}}}}",
        media=f"{{{{N{i}_MEDIA}}}}",
        date_y=f"{{{{N{i}_DATE_Y}}}}",
        date_m=f"{{{{N{i}_DATE_M}}}}",
        date_d=f"{{{{N{i}_DATE_D}}}}",
        body=f"{{{{N{i}_BODY}}}}",
    )
