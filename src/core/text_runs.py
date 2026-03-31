from __future__ import annotations

import re
from typing import List, Tuple

# 简单稳定：中文归 cn，英数归 en，其它符号默认跟随前一个块
_RE = re.compile(r"([\u4e00-\u9fff]+|[A-Za-z0-9]+)", re.UNICODE)

def split_cn_en(text: str) -> List[Tuple[str, str]]:
    """
    把文本切分成 [('cn','...'), ('en','...'), ...]
    - 中文：\u4e00-\u9fff
    - 英文/数字：A-Za-z0-9
    - 标点/空格：跟随前一段（尽量保持视觉一致）
    """
    if not text:
        return []

    parts: List[Tuple[str, str]] = []
    last_end = 0
    last_lang = "cn"

    for m in _RE.finditer(text):
        start, end = m.span()
        # 处理匹配块前面的标点/空格
        if start > last_end:
            gap = text[last_end:start]
            if gap:
                parts.append((last_lang, gap))

        token = m.group(0)
        lang = "cn" if re.match(r"^[\u4e00-\u9fff]+$", token) else "en"
        parts.append((lang, token))
        last_lang = lang
        last_end = end

    # 处理尾巴
    if last_end < len(text):
        tail = text[last_end:]
        parts.append((last_lang, tail))

    return parts
