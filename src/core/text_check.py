from __future__ import annotations

import pycorrector
from typing import List, Tuple


def check_text(text: str) -> List[Tuple[str, str, int]]:
    """
    返回 [(错误词, 建议词, 位置), ...]
    """
    corrected_text, details = pycorrector.correct(text)
    return details