from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class NewsItem:
    topic: str            # 不含【】；输出时模板里已有【】
    title: str            # 标题主体（不含序号、不含【】、不含（媒体 日期））
    media: str            # 媒体名
    source_date: date     # 标题括号内日期
    body: str             # 正文（可含中英文数字）


@dataclass
class Report:
    issue_no: int         # 期号数字
    report_date: date     # 文首日期
    items: list[NewsItem] # 固定10条
