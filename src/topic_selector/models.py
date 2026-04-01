from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class Source:
    key: str
    name_zh: str
    homepage: str
    rss: list[str]
    tier: int
    base_weight: float
    theme_bias: dict[str, float]


@dataclass
class RawArticle:
    source_key: str
    source_name_zh: str
    title: str
    url: str
    published_at: datetime
    summary: str
    content: str


@dataclass
class Candidate:
    article: RawArticle
    labels: list[str] = field(default_factory=list)
    primary_label: str = ""
    score: float = 0.0
    score_breakdown: dict[str, float] = field(default_factory=dict)
    event_key: str = ""
