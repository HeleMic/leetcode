#!/usr/bin/env python3
"""leet — LeetCode workspace CLI.

Usage:
    python3 leet <command> [args]

Commands:
    create:problem <url>   Scaffold a new problem from its LeetCode URL
    test [number]          Run tests (all problems, or a specific one by number)
    help                   Show this message
"""

import sys
from pathlib import Path

# Add the repo root to sys.path so that `cli` and `common` are importable
# regardless of where the script is invoked from.
_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from cli._utils import _die           # noqa: E402
from cli import create_problem        # noqa: E402
from cli import test as _test         # noqa: E402

COMMANDS = {
    "create:problem": create_problem.run,
    "test":           _test.run,
    "help":           lambda _: print(__doc__),
}


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    cmd  = sys.argv[1]
    args = sys.argv[2:]

    if cmd not in COMMANDS:
        available = ", ".join(sorted(COMMANDS))
        _die(f"Unknown command '{cmd}'. Available: {available}")

    COMMANDS[cmd](args)


if __name__ == "__main__":
    main()
