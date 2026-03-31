from __future__ import annotations

import os
from datetime import date

from core.model import Report, NewsItem
from core.docgen import export_report
from core.text_check import check_text


def build_sample_report() -> Report:
    items: list[NewsItem] = []c
    for i in range(1, 11):
        items.append(
            NewsItem(
                topic="示例",
                title=f"示例标题{i} example",
                media="媒体",
                source_date=date(2026, 1, 2),
                body="示例正文：中文mixed with English 123，检查Times New Roman是否生效。",
            )
        )

    return Report(
        issue_no=1,
        report_date=date(2026, 1, 1),
        items=items,
    )


def _print_check_result(idx: int, label: str, details: list[tuple]) -> None:
    """
    details: pycorrector 返回的错误列表，形如 (wrong, correct, start_pos)
    """
    if not details:
        return
    print(f"第{idx}条{label}发现问题（{len(details)}处）：")
    for wrong, right, pos in details:
        print(f"  - 位置{pos}: '{wrong}' -> '{right}'")


def main() -> None:
    print("Running from:", __file__)
    print("Current working directory:", os.getcwd())

    report = build_sample_report()

    print(
        "Report built:",
        report.issue_no,
        report.report_date,
        len(report.items),
    )

    # ===== 文本检查（只提示，不阻断导出、不自动改文）=====
    print("\n开始文本检查（pycorrector，仅提示）...")
    any_issue = False

    for idx, item in enumerate(report.items, start=1):
        title_details = check_text(item.title)
        body_details = check_text(item.body)

        if title_details or body_details:
            any_issue = True
            print(f"\n—— 第{idx}条 ——")
            _print_check_result(idx, "标题", title_details)
            _print_check_result(idx, "正文", body_details)

    if not any_issue:
        print("未发现明显错别字建议。")

    # ===== 导出 =====
    out_path = export_report(report)
    print("\nExported:", out_path)


if __name__ == "__main__":
    main()