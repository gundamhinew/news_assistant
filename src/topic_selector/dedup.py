from __future__ import annotations

import re
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

from rapidfuzz import fuzz

from .models import Candidate


TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "spm"}


def canonical_url(url: str) -> str:
    p = urlparse(url)
    query = [(k, v) for k, v in parse_qsl(p.query, keep_blank_values=True) if k not in TRACKING_PARAMS]
    new_query = urlencode(query)
    return urlunparse((p.scheme, p.netloc.lower(), p.path.rstrip('/'), "", new_query, ""))


def event_key(text: str) -> str:
    text = re.sub(r"\s+", " ", text.lower())
    text = re.sub(r"[^\w\u4e00-\u9fff ]+", "", text)
    tokens = text.split()[:16]
    return "|".join(tokens)


def deduplicate(candidates: list[Candidate], title_threshold: int = 90) -> list[Candidate]:
    by_url: dict[str, Candidate] = {}
    for c in candidates:
        cu = canonical_url(c.article.url)
        if cu not in by_url or c.score > by_url[cu].score:
            by_url[cu] = c

    uniques = list(by_url.values())
    kept: list[Candidate] = []
    for c in sorted(uniques, key=lambda x: x.score, reverse=True):
        sig = event_key(c.article.title + " " + c.article.summary)
        c.event_key = sig
        duplicated = False
        for k in kept:
            tscore = fuzz.ratio(c.article.title, k.article.title)
            if c.event_key == k.event_key or tscore >= title_threshold:
                duplicated = True
                break
        if not duplicated:
            kept.append(c)
    return kept
