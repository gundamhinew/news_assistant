from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .classifier import classify_multilabel, pick_primary_label
from .config import SOURCE_POOL
from .dedup import deduplicate
from .fetchers import fetch_homepage_links, fetch_rss, filter_time_window
from .formatter import render_list
from .models import Candidate
from .ranker import score_candidate, select_balanced


class TopicPipeline:
    def __init__(self) -> None:
        self.sources = SOURCE_POOL

    def run(self, target_big: int = 100, target_small: int = 25) -> tuple[list[Candidate], list[Candidate], str]:
        now_utc = datetime.now(timezone.utc)
        raw = []

        for source in self.sources:
            batch = fetch_rss(source, now_utc)
            if len(batch) < 10:
                batch.extend(fetch_homepage_links(source, now_utc, limit=40))
            raw.extend(batch)

        in_24h = filter_time_window(raw, now_utc, 24)
        pool = in_24h
        if len(in_24h) < 47:
            pool = filter_time_window(raw, now_utc, 48)

        candidates: list[Candidate] = []
        source_by_key = {s.key: s for s in self.sources}
        for article in pool:
            text = f"{article.title} {article.summary} {article.content}"
            labels = classify_multilabel(text)
            c = Candidate(article=article, labels=labels, primary_label=pick_primary_label(labels, text))
            c = score_candidate(c, source_by_key[article.source_key])
            candidates.append(c)

        unique = deduplicate(candidates)
        big = select_balanced(unique, top_n=target_big)
        small = select_balanced(big, top_n=target_small)

        out = render_list(small)
        Path("output").mkdir(exist_ok=True)
        Path("output/candidates_25.txt").write_text(out, encoding="utf-8")
        Path("output/candidates_100.txt").write_text(render_list(big), encoding="utf-8")
        return big, small, out
