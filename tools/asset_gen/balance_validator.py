#!/usr/bin/env python3
"""
balance_validator.py — Compare numeric field values in .dat files before and after the IVAN rewrite.

Fetches old versions from the 'pre-rewrite-checkpoint' git tag and compares them
to current working-tree files. Only balance-critical numeric fields are checked;
name strings and descriptive text are ignored.

Usage:
    python tools/asset_gen/balance_validator.py [--files Script/*.dat] [--output report.txt]

Exit code: 0 if all numeric values match, 1 if any differ.
"""

import re
import subprocess
import sys
import argparse
from collections import defaultdict
from pathlib import Path

# Fields that affect game balance — anything numeric we care about preserving exactly.
BALANCE_FIELDS = {
    "NutritionValue", "StrengthValue", "PriceModifier", "Enchantment",
    "DefenseValue", "WeaponSkillBonus", "AttackStyle", "MinDamage",
    "MaxDamage", "MinDamages", "MaxDamages", "AgilityPenalty",
    "StrengthPenalty", "DexterityBonus", "LuckBonus", "WisdomBonus",
    "CharismaBonus", "IntelligenceBonus", "EnduranceBonus", "ManaBonus",
    "PerceptionBonus", "ArmorClass", "MaxStackSize", "BulkModifier",
    "Flexibility", "Density", "Softness", "SparkleFlags",
    "AttachedGod", "AttribuitesBonus", "AttributeBonus",
    "SpoilModifier", "NutritionModifier", "SpreadChance",
    "SurvivalChance", "DeathSavedByGrace", "Alignment",
    "Times", "Chance", "Weight", "Volume", "Level",
    "StrengthRequirement", "DexterityRequirement", "WillpowerRequirement",
    "HP", "MP", "Speed", "FOVRange", "HearingRange", "TamingDifficulty",
    "XPValue", "Score",
    # Color fields (RGB)
    "Color", "SkinColor", "HairColor", "ClothColor",
    # Weapon-specific
    "BaseToHit", "BaseWillpower", "BaseDexterity", "BaseStrength",
    "BaseEndurance", "BaseAgility", "BasePerception",
}


def get_git_file(git_ref: str, path: str) -> str | None:
    """Return file content at a given git ref, or None if not found."""
    try:
        result = subprocess.run(
            ["git", "show", f"{git_ref}:{path}"],
            capture_output=True, text=True, check=True,
            cwd=Path(path).parent if "/" in path else Path.cwd()
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def get_git_file_from_repo(git_ref: str, repo_path: str, rel_path: str) -> str | None:
    """Return file content at a given git ref from a repo root."""
    try:
        result = subprocess.run(
            ["git", "show", f"{git_ref}:{rel_path}"],
            capture_output=True, text=True, check=True,
            cwd=repo_path
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def extract_numeric_fields(content: str) -> dict[str, list[float]]:
    """
    Extract all occurrences of BalanceField = <number> from .dat content.
    Returns a dict mapping field_name → sorted list of all numeric values found.
    """
    result: dict[str, list[float]] = defaultdict(list)
    # Match: FieldName = number (integer or float, optionally negative)
    pattern = re.compile(r'\b(' + '|'.join(re.escape(f) for f in BALANCE_FIELDS) + r')\s*=\s*(-?\d+(?:\.\d+)?)\s*;', re.MULTILINE)
    for match in pattern.finditer(content):
        field, value = match.group(1), match.group(2)
        result[field].append(float(value))
    for field in result:
        result[field].sort()
    return dict(result)


def extract_rgb_fields(content: str) -> dict[str, list[tuple]]:
    """Extract Color = rgb16(r, g, b) calls."""
    result: dict[str, list[tuple]] = defaultdict(list)
    pattern = re.compile(r'\b(Color|SkinColor|HairColor|ClothColor)\s*=\s*rgb16\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*;')
    for match in pattern.finditer(content):
        field = match.group(1)
        rgb = (int(match.group(2)), int(match.group(3)), int(match.group(4)))
        result[field].append(rgb)
    for field in result:
        result[field].sort()
    return dict(result)


def compare_files(old_content: str, new_content: str, filename: str) -> list[str]:
    """Compare old and new content, returning list of discrepancy messages."""
    issues = []

    old_nums = extract_numeric_fields(old_content)
    new_nums = extract_numeric_fields(new_content)

    all_fields = set(old_nums) | set(new_nums)
    for field in sorted(all_fields):
        old_vals = old_nums.get(field, [])
        new_vals = new_nums.get(field, [])
        if old_vals != new_vals:
            issues.append(
                f"  {field}: old={old_vals} new={new_vals}"
            )

    old_rgb = extract_rgb_fields(old_content)
    new_rgb = extract_rgb_fields(new_content)
    rgb_fields = set(old_rgb) | set(new_rgb)
    for field in sorted(rgb_fields):
        old_vals = old_rgb.get(field, [])
        new_vals = new_rgb.get(field, [])
        if old_vals != new_vals:
            issues.append(
                f"  {field} (rgb16): old count={len(old_vals)} new count={len(new_vals)}"
            )
            if len(old_vals) <= 5 and len(new_vals) <= 5:
                issues.append(f"    old={old_vals}")
                issues.append(f"    new={new_vals}")

    return issues


def find_repo_root(start: Path) -> Path | None:
    p = start.resolve()
    while p != p.parent:
        if (p / ".git").exists():
            return p
        p = p.parent
    return None


def main():
    parser = argparse.ArgumentParser(description="Validate balance-critical numeric values in IVAN .dat files.")
    parser.add_argument("--git-ref", default="pre-rewrite-checkpoint",
                        help="Git ref for the baseline (default: pre-rewrite-checkpoint)")
    parser.add_argument("--files", nargs="*",
                        default=["Script/material.dat", "Script/item.dat", "Script/char.dat"],
                        help=".dat files to validate (relative to repo root)")
    parser.add_argument("--output", default=None, help="Write report to this file instead of stdout")
    args = parser.parse_args()

    repo_root = find_repo_root(Path.cwd())
    if repo_root is None:
        print("ERROR: Not inside a git repository", file=sys.stderr)
        sys.exit(2)

    lines = []
    any_issues = False

    for rel_path in args.files:
        abs_path = repo_root / rel_path
        if not abs_path.exists():
            lines.append(f"SKIP {rel_path} — file not found in working tree")
            continue

        old_content = get_git_file_from_repo(args.git_ref, str(repo_root), rel_path)
        if old_content is None:
            lines.append(f"SKIP {rel_path} — not found in {args.git_ref}")
            continue

        new_content = abs_path.read_text(encoding="utf-8", errors="replace")
        issues = compare_files(old_content, new_content, rel_path)

        if issues:
            any_issues = True
            lines.append(f"FAIL {rel_path} ({len(issues)} discrepanc{'y' if len(issues)==1 else 'ies'}):")
            lines.extend(issues)
        else:
            lines.append(f"OK   {rel_path}")

    lines.append("")
    lines.append("Result: PASS" if not any_issues else "Result: FAIL — numeric balance values changed!")

    report = "\n".join(lines)
    if args.output:
        Path(args.output).write_text(report + "\n")
        print(report)
    else:
        print(report)

    sys.exit(1 if any_issues else 0)


if __name__ == "__main__":
    main()
