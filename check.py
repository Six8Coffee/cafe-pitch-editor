#!/usr/bin/env python3
"""
check.py — verifies Reid's own example transcripts never violate the
no-rewrite, no-generic-phrase, no-drafting-from-nothing rules from rules.md.

This does not run inside a live Claude conversation — nothing does, this is
a plain markdown folder. It's a standalone proof tool: evidence that Reid's
shipped example outputs hold to the rules claimed in rules.md, checkable by
anyone who clones this repo, without having to take rules.md's word for it.

The DRAFTING_INTAKE_PATTERNS category was added after a real failure found
in testing: run in a live environment with broader context loaded, Reid
drifted into asking intake questions ("what format do you want this in?",
"is there an existing draft?") toward drafting a pitch from a blank page —
a different violation of the same no-write doctrine, not caught by the
original two categories. See rules.md, "If there's no draft yet."

Usage:
    python check.py              # scan examples.md for violations
    python check.py --self-test  # confirm the detector itself works
"""

import re
import sys
from pathlib import Path

REWRITE_PATTERNS = [
    r"here'?s a better version",
    r"here'?s how i'?d write it",
    r"try this instead\s*:",
    r"here'?s an example of a better",
    r"here'?s a revised version",
    r"instead, write\s*:",
    r"here'?s what i'?d put",
]

GENERIC_PHRASES = [
    r"consider strengthening",
    r"could be stronger",
    r"try to be more specific",
    r"needs to be more compelling",
    r"you should improve",
    r"make it more engaging",
    r"needs more detail",
]

DRAFTING_INTAKE_PATTERNS = [
    r"is there an existing draft",
    r"or are we starting fresh",
    r"what format (do|would) you want",
    r"what format .* (this|it) (in|be)",
    r"before drafting",
    r"i'?ll draft",
    r"let'?s draft",
    r"here'?s (a |your )?first draft",
    r"what'?s the core ask",
]


def find_violations(text):
    violations = []
    lowered = text.lower()
    for pattern in REWRITE_PATTERNS:
        if re.search(pattern, lowered):
            violations.append(f"rewrite pattern matched: /{pattern}/")
    for pattern in GENERIC_PHRASES:
        if re.search(pattern, lowered):
            violations.append(f"generic phrase matched: /{pattern}/")
    for pattern in DRAFTING_INTAKE_PATTERNS:
        if re.search(pattern, lowered):
            violations.append(f"drafting-intake pattern matched: /{pattern}/")
    return violations


def extract_reid_turns(markdown_text):
    """Split examples.md into Reid's individual turns using the **Reid:** marker."""
    turns = []
    parts = re.split(r"\*\*Reid:\*\*", markdown_text)
    for part in parts[1:]:
        end_match = re.search(r"\*\*Operator:\*\*|\n---|\n##", part)
        turn_text = part[: end_match.start()] if end_match else part
        turns.append(turn_text.strip())
    return turns


def check_examples_file(path):
    text = Path(path).read_text(encoding="utf-8")
    turns = extract_reid_turns(text)
    if not turns:
        print(f"FAIL — no Reid turns found in {path}. Check the **Reid:** marker convention.")
        return False

    all_clean = True
    for i, turn in enumerate(turns, start=1):
        violations = find_violations(turn)
        if violations:
            all_clean = False
            print(f"FAIL — Reid turn {i} contains a violation:")
            for v in violations:
                print(f"   - {v}")
            print(f"   Turn text: {turn[:120]}...")
        else:
            print(f"PASS — Reid turn {i} clean ({len(turn)} chars)")

    print()
    if all_clean:
        print(f"RESULT: all {len(turns)} Reid turns in {path} are clean. No rewrite or generic-phrase violations found.")
    else:
        print("RESULT: violations found. examples.md does not hold to the no-rewrite rule as written.")
    return all_clean


def self_test():
    """Confirm the detector catches known-bad samples and doesn't flag a known-good one."""
    bad_rewrite = (
        "You're right, let me fix that. Here's a better version: "
        "'Common Ground brings honest coffee to Braddon regulars who walk "
        "past three others to get here.'"
    )
    bad_generic = (
        "This section could be stronger. Consider strengthening the "
        "credibility section with more detail."
    )
    good_sample = (
        "This line could describe five hundred cafes. What does a regular "
        "walk past three competitors to get to yours? Name that."
    )
    bad_drafting_intake = (
        "What kind of pitch is this? And what's the context: is there an "
        "existing draft you want me to work from, or are we starting fresh? "
        "What format do you want this pitch in?"
    )
    good_zero_draft_refusal = (
        "Then there's nothing for me to do yet. I edit what's already on "
        "the page — I don't put the first words there. Write a rough first "
        "attempt yourself and bring it back."
    )

    print("Running self-test against known-bad and known-good samples...\n")

    results = []

    v1 = find_violations(bad_rewrite)
    ok1 = len(v1) > 0
    results.append(ok1)
    print(f"{'PASS' if ok1 else 'FAIL'} — rewrite sample correctly {'flagged' if ok1 else 'MISSED'}")

    v2 = find_violations(bad_generic)
    ok2 = len(v2) > 0
    results.append(ok2)
    print(f"{'PASS' if ok2 else 'FAIL'} — generic-phrase sample correctly {'flagged' if ok2 else 'MISSED'}")

    v3 = find_violations(good_sample)
    ok3 = len(v3) == 0
    results.append(ok3)
    label = "left alone" if ok3 else f"FALSE POSITIVE: {v3}"
    print(f"{'PASS' if ok3 else 'FAIL'} — clean sample correctly {label}")

    v4 = find_violations(bad_drafting_intake)
    ok4 = len(v4) > 0
    results.append(ok4)
    print(f"{'PASS' if ok4 else 'FAIL'} — drafting-intake sample correctly {'flagged' if ok4 else 'MISSED'}")

    v5 = find_violations(good_zero_draft_refusal)
    ok5 = len(v5) == 0
    results.append(ok5)
    label5 = "left alone" if ok5 else f"FALSE POSITIVE: {v5}"
    print(f"{'PASS' if ok5 else 'FAIL'} — correct zero-draft refusal correctly {label5}")

    print()
    if all(results):
        print("SELF-TEST RESULT: detector works — catches real violations, doesn't flag clean critique.")
    else:
        print("SELF-TEST RESULT: detector is broken. Do not trust a clean run against examples.md until this is fixed.")
    return all(results)


def main():
    if "--self-test" in sys.argv:
        ok = self_test()
        sys.exit(0 if ok else 1)

    examples_path = Path(__file__).parent / "examples.md"
    ok = check_examples_file(examples_path)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
