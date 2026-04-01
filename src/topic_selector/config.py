from __future__ import annotations

from .models import Source

TOPICS = [
    "国际政治",
    "金融稳定",
    "宏观经济",
    "全球贸易",
    "全球失衡",
    "能源矿产",
    "产业经济",
    "科技产业",
    "军事防务",
    "主权债务",
]

SOURCE_POOL: list[Source] = [
    Source("reuters", "路透", "https://www.reuters.com", ["https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best", "https://feeds.reuters.com/reuters/worldNews"], 1, 1.0, {"国际政治": 1.0, "金融稳定": 1.0, "宏观经济": 0.9, "全球贸易": 0.9, "主权债务": 0.9}),
    Source("bloomberg", "彭博", "https://www.bloomberg.com", ["https://feeds.bloomberg.com/markets/news.rss", "https://feeds.bloomberg.com/economics/news.rss"], 1, 0.98, {"金融稳定": 1.0, "宏观经济": 1.0, "科技产业": 0.8, "主权债务": 0.9}),
    Source("aljazeera", "半岛电视台", "https://www.aljazeera.com", ["https://www.aljazeera.com/xml/rss/all.xml"], 1, 0.9, {"国际政治": 1.0, "军事防务": 0.9, "能源矿产": 0.8}),
    Source("ft", "金融时报", "https://www.ft.com", ["https://www.ft.com/world?format=rss", "https://www.ft.com/markets?format=rss"], 1, 0.88, {"金融稳定": 1.0, "宏观经济": 0.9, "国际政治": 0.8}),
    Source("ap", "美联社", "https://apnews.com", ["https://apnews.com/hub/apf-topnews?output=amp"], 1, 0.86, {"国际政治": 1.0, "军事防务": 0.8}),
    Source("wsj", "华尔街日报", "https://www.wsj.com", [], 1, 0.84, {"金融稳定": 1.0, "宏观经济": 0.9, "国际政治": 0.6}),
    Source("washingtonpost", "华盛顿邮报", "https://www.washingtonpost.com", [], 1, 0.8, {"国际政治": 0.9}),
    Source("nytimes", "纽约时报", "https://www.nytimes.com", ["https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "https://rss.nytimes.com/services/xml/rss/nyt/Economy.xml"], 1, 0.8, {"国际政治": 0.9, "宏观经济": 0.8}),
    Source("scmp", "南华早报", "https://www.scmp.com", [], 1, 0.82, {"科技产业": 0.9, "宏观经济": 0.9, "军事防务": 0.8}),
    Source("nikkei", "日经新闻", "https://asia.nikkei.com", ["https://asia.nikkei.com/rss/feed/nar"], 1, 0.82, {"主权债务": 0.9, "全球贸易": 0.8, "产业经济": 0.9}),
    Source("bbc", "英国广播公司", "https://www.bbc.com", ["https://feeds.bbci.co.uk/news/world/rss.xml", "https://feeds.bbci.co.uk/news/business/rss.xml"], 1, 0.8, {"国际政治": 0.9, "宏观经济": 0.7}),
    Source("zaobao", "联合早报", "https://www.zaobao.com", [], 1, 0.78, {"国际政治": 0.8, "宏观经济": 0.8}),
    Source("politico", "Politico", "https://www.politico.com", ["https://www.politico.com/rss/politicopicks.xml"], 1, 0.76, {"国际政治": 1.0, "军事防务": 0.7}),
    Source("defensenews", "Defense News", "https://www.defensenews.com", ["https://www.defensenews.com/arc/outboundfeeds/rss/category/global/"], 1, 0.74, {"军事防务": 1.0}),
    Source("techcrunch", "TechCrunch", "https://techcrunch.com", ["https://techcrunch.com/feed/"], 1, 0.74, {"科技产业": 1.0}),
    Source("rfi_afrique", "RFI非洲板块", "https://www.rfi.fr/cn/非洲", ["https://www.rfi.fr/fr/afrique/rss"], 1, 0.72, {"主权债务": 0.9, "国际政治": 0.7}),
]

SENSITIVE_EXCLUDE_KEYWORDS = [
    "中国党内",
    "中共高层内斗",
    "中国领土争议",
]

CHINA_ALLOWED_KEYWORDS = [
    "中国经济", "中国金融", "中国科技", "中国外交", "中国军工", "中国装备",
]
