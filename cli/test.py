"""test — run tests for all problems or a specific one."""

import importlib.util
import json
import sys
from pathlib import Path

from cli._utils import _die

REPO_ROOT = Path(__file__).parent.parent
PROBLEMS_DIR = REPO_ROOT / "problems"

SEP_THIN  = "─" * 52
SEP_THICK = "═" * 52

NORMALIZERS = {
    "sort":        lambda x: sorted(x) if isinstance(x, list) else x,
    "sort_nested": lambda x: sorted(sorted(r) for r in x) if isinstance(x, list) else x,
    "set":         lambda x: frozenset(x) if isinstance(x, list) else x,
}

_common_cache: dict = {}


def _common(name: str):
    if name not in _common_cache:
        import importlib
        mod = importlib.import_module("common")
        _common_cache[name] = getattr(mod, name)
    return _common_cache[name]


def _coerce(value, type_str: str | None):
    """Convert a JSON-decoded value to the expected Python type."""
    if type_str == "ListNode":
        return _common("ListNode").from_list(value)
    if type_str == "TreeNode":
        return _common("TreeNode").from_list(value)
    return value


def _serialize(value, type_str: str | None):
    """Convert a result value back to a JSON-comparable form."""
    if type_str == "ListNode" and value is not None:
        return value.to_list()
    if type_str == "TreeNode" and value is not None:
        return value.to_list()
    return value


def _load_solution(problem_dir: Path):
    spec = importlib.util.spec_from_file_location("solution", problem_dir / "solution.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Solution()


def _run_problem(problem_dir: Path) -> tuple[int, int]:
    tests_file = problem_dir / "tests.json"
    if not tests_file.exists() or not (problem_dir / "solution.py").exists():
        return 0, 0

    with open(tests_file) as f:
        data = json.load(f)

    method_name = data["method"]
    param_types = data.get("param_types")
    return_type = data.get("return_type")
    normalizer  = NORMALIZERS.get(data.get("normalizer")) if data.get("normalizer") else None
    cases       = data["cases"]

    solution = _load_solution(problem_dir)
    method   = getattr(solution, method_name)

    passed = failed = 0
    print(f"\n{SEP_THIN}")
    print(f"  {problem_dir.name}")
    print(SEP_THIN)

    for i, case in enumerate(cases, 1):
        raw_args, expected = case["args"], case["expected"]
        label = case.get("label", f"Case {i}")

        call_args = (
            [_coerce(v, param_types[j] if j < len(param_types) else None)
             for j, v in enumerate(raw_args)]
            if param_types else raw_args
        )

        try:
            result = method(*call_args)
        except Exception as e:
            print(f"  ✗ {label}  →  ERROR: {e}")
            failed += 1
            continue

        result_cmp = _serialize(result, return_type)
        r = normalizer(result_cmp) if normalizer else result_cmp
        e = normalizer(expected)   if normalizer else expected

        if r == e:
            print(f"  ✓ {label}")
            passed += 1
        else:
            print(f"  ✗ {label}")
            print(f"      args:     {raw_args}")
            print(f"      expected: {expected}")
            print(f"      got:      {result_cmp}")
            failed += 1

    return passed, failed


def _find_dir(number: str) -> Path | None:
    matches = sorted(PROBLEMS_DIR.glob(f"{number.zfill(4)}-*"))
    return matches[0] if matches else None


# ── Entry point ───────────────────────────────────────────────────────────────

def run(args: list[str]) -> None:
    if args:
        d = _find_dir(args[0])
        if not d:
            _die(f"Problem '{args[0]}' not found.")
        dirs = [d]
    else:
        dirs = sorted(d for d in PROBLEMS_DIR.iterdir() if d.is_dir())

    total_p = total_f = 0
    for d in dirs:
        p, f = _run_problem(d)
        total_p += p
        total_f += f

    print(f"\n{SEP_THICK}")
    status = "✓ All passed" if total_f == 0 else f"✗ {total_f} failed"
    print(f"  {status}  ({total_p} passed, {total_f} failed)")
    print(f"{SEP_THICK}\n")

    if total_f:
        sys.exit(1)
