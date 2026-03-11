#!/usr/bin/env python3
"""Test runner for LeetCode solutions.

Usage:
    python3 run_tests.py           # run all tests
    python3 run_tests.py 1         # run tests for problem 1
    python3 run_tests.py 0001      # same as above

tests.json schema (per problem):
    {
        "method": "<LeetCode method name>",
        "normalizer": "sort",       // optional: normalize output before comparing
        "cases": [
            {
                "label": "Human-readable description",
                "args": [<positional arg1>, <positional arg2>, ...],
                "expected": <expected return value>
            }
        ]
    }

Available normalizers:
    sort          — sorted(result)  (for "any order" list outputs)
    sort_nested   — sorted([sorted(row) for row in result])  (list of lists)
    set           — frozenset(result)  (unordered, no duplicates)
"""

import sys
import json
import importlib.util
from pathlib import Path

PROBLEMS_DIR = Path(__file__).parent / "problems"
SEP_THIN = "─" * 52
SEP_THICK = "═" * 52

NORMALIZERS = {
    "sort": lambda x: sorted(x) if isinstance(x, list) else x,
    "sort_nested": lambda x: sorted(sorted(row) for row in x) if isinstance(x, list) else x,
    "set": lambda x: frozenset(x) if isinstance(x, list) else x,
}


def load_solution(problem_dir: Path):
    spec = importlib.util.spec_from_file_location(
        "solution", problem_dir / "solution.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Solution()


def run_problem_tests(problem_dir: Path) -> tuple[int, int]:
    tests_file = problem_dir / "tests.json"
    solution_file = problem_dir / "solution.py"

    if not tests_file.exists() or not solution_file.exists():
        return 0, 0

    with open(tests_file) as f:
        data = json.load(f)

    method_name = data["method"]
    normalizer_key = data.get("normalizer")
    normalizer = NORMALIZERS.get(normalizer_key) if normalizer_key else None
    cases = data["cases"]

    solution = load_solution(problem_dir)
    method = getattr(solution, method_name)

    passed = 0
    failed = 0

    print(f"\n{SEP_THIN}")
    print(f"  {problem_dir.name}")
    print(SEP_THIN)

    for i, case in enumerate(cases, 1):
        args = case["args"]
        expected = case["expected"]

        try:
            result = method(*args)
        except Exception as e:
            print(f"  ✗ Case {i}  →  ERROR: {e}")
            failed += 1
            continue

        if normalizer:
            result_cmp = normalizer(result)
            expected_cmp = normalizer(expected)
        else:
            result_cmp = result
            expected_cmp = expected

        label = case.get("label", f"Case {i}")
        if result_cmp == expected_cmp:
            print(f"  ✓ {label}")
            passed += 1
        else:
            print(f"  ✗ {label}")
            print(f"      args:     {args}")
            print(f"      expected: {expected}")
            print(f"      got:      {result}")
            failed += 1

    return passed, failed


def find_problem_dir(number: str) -> Path | None:
    padded = number.zfill(4)
    matches = sorted(PROBLEMS_DIR.glob(f"{padded}-*"))
    return matches[0] if matches else None


def main():
    if len(sys.argv) > 1:
        number = sys.argv[1]
        problem_dir = find_problem_dir(number)
        if not problem_dir:
            print(f"Problem '{number}' not found.")
            sys.exit(1)
        dirs = [problem_dir]
    else:
        dirs = sorted(d for d in PROBLEMS_DIR.iterdir() if d.is_dir())

    total_passed = 0
    total_failed = 0

    for d in dirs:
        p, f = run_problem_tests(d)
        total_passed += p
        total_failed += f

    print(f"\n{SEP_THICK}")
    status = "✓ All passed" if total_failed == 0 else f"✗ {total_failed} failed"
    print(f"  {status}  ({total_passed} passed, {total_failed} failed)")
    print(f"{SEP_THICK}\n")

    if total_failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
