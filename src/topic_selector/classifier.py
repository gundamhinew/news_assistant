from __future__ import annotations

import re
from collections import defaultdict

from .config import TOPICS

TOPIC_KEYWORDS: dict[str, list[str]] = {
    "国际政治": ["外交", "制裁", "停火", "谈判", "峰会", "大选", "冲突", "政局", "联合国"],
    "金融稳定": ["银行", "流动性", "系统性风险", "金融监管", "信用风险", "挤兑", "救助"],
    "宏观经济": ["通胀", "就业", "货币政策", "财政", "增长", "房地产", "消费", "投资"],
    "全球贸易": ["关税", "出口", "进口", "贸易摩擦", "航运", "贸易协定", "贸易限制"],
    "全球失衡": ["经常账户", "贸易顺差", "贸易逆差", "失衡", "再平衡"],
    "能源矿产": ["石油", "天然气", "煤炭", "电力", "铀", "铜", "锂", "稀土"],
    "产业经济": ["汽车", "钢铁", "造船", "化工", "机械", "制造业", "产业链"],
    "科技产业": ["半导体", "人工智能", "云计算", "通信", "平台", "芯片", "算力"],
    "军事防务": ["军援", "军购", "导弹", "演习", "防务预算", "部署", "军工"],
    "主权债务": ["债务", "违约", "评级", "重组", "imf", "国际货币基金组织", "外汇储备", "偿债"],
}

DEVELOPING_HINTS = ["巴基斯坦", "埃及", "加纳", "斯里兰卡", "肯尼亚", "赞比亚", "阿根廷", "尼日利亚"]


def classify_multilabel(text: str) -> list[str]:
    text_l = text.lower()
    scores = defaultdict(float)

    for topic in TOPICS:
        for kw in TOPIC_KEYWORDS.get(topic, []):
            if kw.lower() in text_l:
                scores[topic] += 1.0

    # 主权债务特殊增强：发展中国家宏观+债务相关自动上浮
    if any(c.lower() in text_l for c in [x.lower() for x in DEVELOPING_HINTS]):
        if re.search(r"债务|融资|评级|imf|外汇|偿债|重组", text_l):
            scores["主权债务"] += 2.0

    labels = [k for k, v in scores.items() if v >= 1.0]
    return labels or ["国际政治"]


def pick_primary_label(labels: list[str], text: str) -> str:
    text_l = text.lower()
    best = labels[0]
    best_score = -1.0
    for label in labels:
        s = 0.0
        for kw in TOPIC_KEYWORDS.get(label, []):
            if kw.lower() in text_l:
                s += 1.0
        if s > best_score:
            best, best_score = label, s
    return best
