from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable

import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil import parser as dt_parser

from .models import RawArticle, Source

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = dt_parser.parse(value)
    except Exception:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def fetch_rss(source: Source, now_utc: datetime) -> list[RawArticle]:
    results: list[RawArticle] = []
    for rss_url in source.rss:
        try:
            feed = feedparser.parse(rss_url)
        except Exception:
            continue

        for entry in feed.entries[:80]:
            title = (entry.get("title") or "").strip()
            link = (entry.get("link") or "").strip()
            summary = (entry.get("summary") or "").strip()
            published = _parse_dt(entry.get("published") or entry.get("updated")) or now_utc
            if not title or not link:
                continue
            results.append(
                RawArticle(
                    source_key=source.key,
                    source_name_zh=source.name_zh,
                    title=title,
                    url=link,
                    published_at=published,
                    summary=summary,
                    content=summary,
                )
            )
    return results


def fetch_homepage_links(source: Source, now_utc: datetime, limit: int = 25) -> list[RawArticle]:
    """RSS缺失时的兜底抓取。"""
    try:
        resp = requests.get(source.homepage, headers={"User-Agent": UA}, timeout=15)
        resp.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    results: list[RawArticle] = []
    seen: set[str] = set()
    for a in soup.select("a[href]"):
        href = a.get("href", "").strip()
        title = a.get_text(" ", strip=True)
        if not href or not title:
            continue
        if href.startswith("/"):
            href = source.homepage.rstrip("/") + href
        if not href.startswith("http"):
            continue
        if href in seen:
            continue
        seen.add(href)
        results.append(
            RawArticle(
                source_key=source.key,
                source_name_zh=source.name_zh,
                title=title,
                url=href,
                published_at=now_utc,
                summary="",
                content=title,
            )
        )
        if len(results) >= limit:
            break
    return results


def filter_time_window(articles: Iterable[RawArticle], now_utc: datetime, hours: int) -> list[RawArticle]:
    threshold = now_utc - timedelta(hours=hours)
    return [a for a in articles if a.published_at >= threshold]
