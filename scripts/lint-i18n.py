#!/usr/bin/env python3
"""Structural EN/DE parity lint for the bilingual site.

Checks paired YAML files, the i18n UI strings, news entries, paired Markdown
nav pages, and member CVs. Also warns when an EN file is significantly newer
than its DE counterpart. Exits 1 on any failure, 0 otherwise (warnings only).
Use --strict to also fail on staleness warnings.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent

# Top-of-file config — promote to a config file only if a third language is added.

PAIRED_YAML = [
    ("_data/cv.yaml", "_data/cv_de.yaml"),
]

PAIRED_PAGES = [
    "index.md",
    "research/index.md",
    "projects/index.md",
    "team/index.md",
]

LEADER_MEMBER_EN = "_members/adrien-florio.md"
LEADER_MEMBER_DE = "_members/adrien-florio.de.md"

STALE_DAYS = 14


errors: list[tuple[str, str]] = []
warnings: list[tuple[str, str]] = []


def err(section: str, message: str) -> None:
    errors.append((section, message))
    print(f"  FAIL: {message}")


def warn(section: str, message: str) -> None:
    warnings.append((section, message))
    print(f"  WARN: {message}")


def ok(message: str) -> None:
    print(f"  ok:   {message}")


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_front_matter(path: Path) -> dict:
    """Return parsed Jekyll front matter, or {} if absent."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            data = yaml.safe_load("\n".join(lines[1:i]))
            return data if isinstance(data, dict) else {}
    return {}


def walk_pair(en, de, path: str, section: str) -> None:
    """Recursively compare keys of paired YAML structures.

    Dicts: keys must match. Lists: lengths must match, recurse pairwise by
    index. Scalars: not compared (translations differ by definition).
    """
    if isinstance(en, dict) and isinstance(de, dict):
        en_keys = set(en.keys())
        de_keys = set(de.keys())
        for k in sorted(en_keys - de_keys):
            err(section, f"{path}: key '{k}' present in EN but missing in DE")
        for k in sorted(de_keys - en_keys):
            err(section, f"{path}: key '{k}' present in DE but missing in EN")
        for k in sorted(en_keys & de_keys):
            walk_pair(en[k], de[k], f"{path}.{k}", section)
    elif isinstance(en, list) and isinstance(de, list):
        if len(en) != len(de):
            err(section, f"{path}: list length mismatch (EN={len(en)}, DE={len(de)})")
        for i, (ev, dv) in enumerate(zip(en, de)):
            walk_pair(ev, dv, f"{path}[{i}]", section)


def check_paired_yaml() -> None:
    section = "Paired YAML files"
    print(f"\n== {section} ==")
    for en_rel, de_rel in PAIRED_YAML:
        en_path = REPO_ROOT / en_rel
        de_path = REPO_ROOT / de_rel
        if not en_path.exists():
            err(section, f"{en_rel}: file missing")
            continue
        if not de_path.exists():
            err(section, f"{de_rel}: file missing")
            continue
        before = len(errors)
        walk_pair(load_yaml(en_path), load_yaml(de_path), f"{en_rel} ↔ {de_rel}", section)
        if len(errors) == before:
            ok(f"{en_rel} ↔ {de_rel}")


def check_i18n_yaml() -> None:
    section = "_data/i18n.yaml"
    print(f"\n== {section} ==")
    path = REPO_ROOT / "_data/i18n.yaml"
    if not path.exists():
        err(section, "_data/i18n.yaml: file missing")
        return
    data = load_yaml(path) or {}
    en = data.get("en") or {}
    de = data.get("de") or {}
    en_keys = set(en.keys())
    de_keys = set(de.keys())
    mismatched = False
    for k in sorted(en_keys - de_keys):
        err(section, f"key '{k}' present in en: but missing in de:")
        mismatched = True
    for k in sorted(de_keys - en_keys):
        err(section, f"key '{k}' present in de: but missing in en:")
        mismatched = True
    if not mismatched:
        ok(f"en/de keys match ({len(en_keys)} keys)")


def check_news_yaml() -> None:
    section = "_data/news.yaml"
    print(f"\n== {section} ==")
    path = REPO_ROOT / "_data/news.yaml"
    if not path.exists():
        err(section, "_data/news.yaml: file missing")
        return
    data = load_yaml(path) or []
    ok_count = 0
    skip_count = 0
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            err(section, f"entry #{i}: not a mapping")
            continue
        ident = entry.get("date", f"entry #{i}")
        if entry.get("translate") is False:
            skip_count += 1
            continue
        missing = []
        if not entry.get("text"):
            missing.append("text")
        if not entry.get("text_de"):
            missing.append("text_de")
        if missing:
            err(section, f"entry {ident}: missing {', '.join(missing)} (or set translate: false)")
        else:
            ok_count += 1
    ok(f"{ok_count} translated, {skip_count} skipped (translate: false)")


def check_paired_pages() -> None:
    section = "Paired Markdown pages"
    print(f"\n== {section} ==")
    for rel in PAIRED_PAGES:
        en_path = REPO_ROOT / rel
        de_path = REPO_ROOT / "de" / rel
        if not en_path.exists():
            err(section, f"{rel}: EN file missing")
            continue
        fm = parse_front_matter(en_path)
        if fm.get("translate") is False:
            ok(f"{rel} (translate: false)")
            continue
        if not de_path.exists():
            err(section, f"{rel}: DE counterpart missing at de/{rel}")
        else:
            ok(f"{rel} ↔ de/{rel}")


def check_member_cvs() -> None:
    section = "Member CVs"
    print(f"\n== {section} ==")
    members_dir = REPO_ROOT / "_members"
    leader_de = REPO_ROOT / LEADER_MEMBER_DE
    for member in sorted(members_dir.glob("*.md")):
        if member.name.endswith(".de.md"):
            continue
        rel = member.relative_to(REPO_ROOT).as_posix()
        if rel == LEADER_MEMBER_EN:
            if not leader_de.exists():
                err(section, f"{rel}: required DE mirror missing at {LEADER_MEMBER_DE}")
            else:
                ok(f"{rel} ↔ {LEADER_MEMBER_DE}")
        else:
            fm = parse_front_matter(member)
            if fm.get("translate") is False:
                ok(f"{rel} (translate: false)")
            else:
                err(section, f"{rel}: non-leader member must set translate: false in front matter")


def git_mtime(rel: str) -> int | None:
    """Last commit timestamp for `rel`, or None if untracked / no history."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "--", rel],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    out = result.stdout.strip()
    if not out:
        return None
    try:
        return int(out)
    except ValueError:
        return None


def check_staleness() -> None:
    section = "Staleness"
    print(f"\n== {section} (threshold: {STALE_DAYS} days) ==")
    pairs: list[tuple[str, str]] = []
    pairs.extend(PAIRED_YAML)
    pairs.append((LEADER_MEMBER_EN, LEADER_MEMBER_DE))
    for rel in PAIRED_PAGES:
        pairs.append((rel, f"de/{rel}"))
    for en_rel, de_rel in pairs:
        en_path = REPO_ROOT / en_rel
        de_path = REPO_ROOT / de_rel
        if not en_path.exists() or not de_path.exists():
            continue
        en_t = git_mtime(en_rel)
        de_t = git_mtime(de_rel)
        if en_t is None or de_t is None:
            ok(f"{en_rel} ↔ {de_rel} (no git history yet)")
            continue
        delta_days = (en_t - de_t) / 86400.0
        if delta_days > STALE_DAYS:
            warn(section, f"{en_rel} is {delta_days:.1f} days newer than {de_rel}")
        else:
            ok(f"{en_rel} ↔ {de_rel} (Δ {delta_days:+.1f} days)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Structural EN/DE parity lint.")
    parser.add_argument("--strict", action="store_true", help="Also fail on staleness warnings.")
    args = parser.parse_args()

    check_paired_yaml()
    check_i18n_yaml()
    check_news_yaml()
    check_paired_pages()
    check_member_cvs()
    check_staleness()

    print("\n== Summary ==")
    print(f"  errors:   {len(errors)}")
    print(f"  warnings: {len(warnings)}")

    if errors:
        return 1
    if args.strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
