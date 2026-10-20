#!/usr/bin/env python3
"""聚合账户级仓库统计（公开 + 私密）。

边界：
- 只调用 /user/repos 与 /repos/{owner}/{repo}/languages
- 不下载、不读取任何仓库文件内容
- 输出只含聚合数字，不含私库名称
"""

import json
import os
import sys
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone

TOKEN = os.environ.get("METRICS_TOKEN")
if not TOKEN:
    sys.exit("METRICS_TOKEN 未设置")

API = "https://api.github.com"


def api_get(path: str):
    req = urllib.request.Request(
        API + path,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "juice094-stats",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def list_owned_repos():
    repos, page = [], 1
    while True:
        batch = api_get(f"/user/repos?affiliation=owner&per_page=100&page={page}")
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def main():
    repos = list_owned_repos()
    public = sum(1 for r in repos if not r["private"])
    private = sum(1 for r in repos if r["private"])
    total_size_kb = sum(r.get("size", 0) for r in repos)

    lang_bytes = defaultdict(int)
    skipped = 0
    for r in repos:
        owner, name = r["owner"]["login"], r["name"]
        try:
            langs = api_get(f"/repos/{owner}/{name}/languages")
        except urllib.error.HTTPError as e:
            skipped += 1
            print(f"skip {name}: HTTP {e.code}", file=sys.stderr)
            continue
        for lang, b in langs.items():
            lang_bytes[lang] += b

    total_bytes = sum(lang_bytes.values()) or 1
    languages = {
        lang: {"bytes": b, "percent": round(b * 100 / total_bytes, 2)}
        for lang, b in sorted(lang_bytes.items(), key=lambda x: -x[1])
    }

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "summary": {
            "total_repos": len(repos),
            "public_repos": public,
            "private_repos": private,
            "total_size_kb": total_size_kb,
            "skipped_repos": skipped,
        },
        "languages": languages,
    }

    os.makedirs("profile", exist_ok=True)
    with open("profile/stats.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(json.dumps(out["summary"], ensure_ascii=False))


if __name__ == "__main__":
    main()
