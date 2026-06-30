#!/usr/bin/env python3
"""
简历构建脚本

用法：
    python resume/build.py --config general
    python resume/build.py --config damo
    python resume/build.py --all

说明：
    读取 resume/data/resume.yaml 作为单一数据源，
    根据 resume/configs/<config>.yaml 的定向配置，
    使用 Jinja2 模板渲染生成定向简历 Markdown。
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).parent.resolve()
DATA_DIR = ROOT / "data"
CONFIG_DIR = ROOT / "configs"
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "output"


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def filter_by_tags(bullets, emphasis_tags):
    """根据 emphasis_tags 筛选 bullet，保留最相关的条目。"""
    if not emphasis_tags:
        return bullets

    scored = []
    for bullet in bullets:
        tags = set(bullet.get("tags", []))
        score = len(tags & set(emphasis_tags))
        scored.append((score, bullet))

    # 按匹配分数降序，分数相同保持原顺序
    scored.sort(key=lambda x: (-x[0], bullets.index(x[1])))
    return [b for _, b in scored]


def limit(items, n):
    """限制列表长度。"""
    return items[: int(n)]


def clean_markdown(text: str) -> str:
    """清理 Markdown 中的多余空行，保持段落间一个空行。"""
    import re

    # 把 3 个及以上连续换行替换为 2 个换行
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 去掉行尾空格
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text.strip() + "\n"


def render_resume(config_name: str) -> Path:
    """渲染指定配置的简历 Markdown。"""
    data = load_yaml(DATA_DIR / "resume.yaml")
    config = load_yaml(CONFIG_DIR / f"{config_name}.yaml")

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    env.filters["filter_by_tags"] = filter_by_tags
    env.filters["limit"] = limit

    template = env.get_template("resume.md.j2")

    # 合并数据和配置作为模板上下文
    context = {**data, **config}

    # 处理 skills：如果配置指定了 categories，则筛选
    skill_categories = config.get("skill_categories", "all")
    if skill_categories != "all":
        context["skills"] = [
            s for s in data["skills"] if s["category"] in skill_categories
        ]

    # 处理项目顺序
    project_order = config.get("project_order", [p["name"] for p in data["projects"]])
    context["project_order"] = project_order

    markdown = template.render(context)
    markdown = clean_markdown(markdown)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_md = OUTPUT_DIR / f"{config_name}.md"
    with open(output_md, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"Generated: {output_md}")
    return output_md


def build_all():
    """构建所有配置。"""
    for config_file in sorted(CONFIG_DIR.glob("*.yaml")):
        config_name = config_file.stem
        render_resume(config_name)


def build_pdf(md_path: Path) -> Path:
    """使用 pandoc + typst 将 Markdown 转为 PDF。"""
    pdf_path = md_path.with_suffix(".pdf")
    cmd = [
        "pandoc",
        str(md_path),
        "-o",
        str(pdf_path),
        "--pdf-engine=typst",
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated: {pdf_path}")
    return pdf_path


def main():
    parser = argparse.ArgumentParser(description="Build resumes from YAML data")
    parser.add_argument("--config", help="Config name, e.g. general or damo")
    parser.add_argument("--all", action="store_true", help="Build all configs")
    parser.add_argument("--pdf", action="store_true", help="Also generate PDF via pandoc+typst")
    args = parser.parse_args()

    if args.all:
        for config_file in sorted(CONFIG_DIR.glob("*.yaml")):
            config_name = config_file.stem
            md = render_resume(config_name)
            if args.pdf:
                build_pdf(md)
    elif args.config:
        md = render_resume(args.config)
        if args.pdf:
            build_pdf(md)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
