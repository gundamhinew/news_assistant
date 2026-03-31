from __future__ import annotations
from pathlib import Path

# 项目根目录 = src 的上一级
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 固定条数
NEWS_COUNT = 10

# 模板与输出位置（先按相对路径）
TEMPLATE_PATH = str(PROJECT_ROOT / "templates" / "template_master.docx")
OUTPUT_DIR = str(PROJECT_ROOT / "output")

# 输出文件名模板：YYYYMMDD 国际要闻摘编.docx
OUTPUT_NAME_FMT = "{yyyymmdd} 国际要闻摘编.docx"

# 字体名（必须与 Word 中字体名称一致；后续 docgen 会用到）
FONT_CN_TITLE = "方正小标宋_GBK"
FONT_CN_HEAD = "方正黑体_GBK"
FONT_CN_BODY = "仿宋_GB2312"
FONT_EN = "Times New Roman"

# Word 三号大约为 16pt（后续写 run 会用到）
FONT_SIZE_PT_SANHAO = 16
