from __future__ import annotations

from collections import Counter

from .models import Candidate, Source


def score_candidate(c: Candidate, source: Source) -> Candidate:
    text = f"{c.article.title} {c.article.summary} {c.article.content}".lower()
    score_breakdown: dict[str, float] = {}

    source_score = source.base_weight * 30
    score_breakdown["source"] = source_score

    topic_score = 0.0
    for label in c.labels:
        topic_score += source.theme_bias.get(label, 0.4) * 10
    score_breakdown["topic_match"] = topic_score

    recency_bonus = 10.0
    score_breakdown["recency"] = recency_bonus

    exclusive_bonus = 6.0 if any(k in text for k in ["exclusive", "独家", "investigation", "调查"]) else 0.0
    score_breakdown["exclusive"] = exclusive_bonus

    sensitivity_penalty = 0.0
    if any(k in text for k in ["中国党内", "领土争议"]):
        sensitivity_penalty = -30.0
    score_breakdown["sensitivity"] = sensitivity_penalty

    c.score_breakdown = score_breakdown
    c.score = sum(score_breakdown.values())
    return c


def select_balanced(candidates: list[Candidate], top_n: int) -> list[Candidate]:
    picked: list[Candidate] = []
    source_counter = Counter()
    topic_counter = Counter()

    for c in sorted(candidates, key=lambda x: x.score, reverse=True):
        if len(picked) >= top_n:
            break
        if source_counter[c.article.source_key] >= max(8, top_n // 4):
            continue
        if topic_counter[c.primary_label] >= max(12, top_n // 2):
            continue
        picked.append(c)
        source_counter[c.article.source_key] += 1
        topic_counter[c.primary_label] += 1

    if len(picked) < top_n:
        remaining = [x for x in sorted(candidates, key=lambda x: x.score, reverse=True) if x not in picked]
        picked.extend(remaining[: top_n - len(picked)])

    return picked
