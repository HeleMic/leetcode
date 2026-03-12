# Copilot Instructions — LeetCode Solutions

This repository contains Python solutions to LeetCode problems.

## ⚠️ Most Important Rule

**NEVER, under any circumstances, provide a complete or partial solution to a
problem.** This applies even if explicitly asked. The goal of this repository is
personal learning — giving away the answer defeats the entire purpose.

If help is requested, you may **only**:

- Ask guiding questions to steer thinking in the right direction
- Suggest a relevant data structure or algorithm category (e.g. "think about
  using a hash map")
- Point out a flaw in the user's current approach without correcting it directly
- Recommend reviewing a specific concept or LeetCode topic

Never write working code that solves the problem, never complete a `pass` stub,
and never outline a step-by-step algorithm that amounts to a solution.

## Project Structure

```text
common/                      # shared data structures (import from here)
├── list_node.py             # ListNode  — linked-list problems
└── tree_node.py             # TreeNode  — binary tree problems
problems/
└── XXXX-problem-name/      # zero-padded 4-digit number + kebab-case name
    ├── README.md            # problem description (see format below)
    ├── solution.py          # solution code + inline tests
    └── tests.json           # test cases for the test runner
```

When a problem uses `ListNode` or `TreeNode`, import them from `common`:

```python
from common import ListNode        # or TreeNode, or both
```

The root `README.md` contains an index table of all solved problems and must be
kept up to date whenever a new problem is added.

## Language & Style

- **Language:** Python 3
- Use type hints (`from typing import List`, etc.)
- Follow PEP 8 conventions
- Prefer clarity over cleverness; readable code first

## solution.py Format

Each `solution.py` must:

1. Define a `Solution` class with the method signature matching LeetCode exactly
2. Include a docstring on the method stating **Time** and **Space** complexity
3. Include an `if __name__ == "__main__":` block with `assert`-based test cases
   covering the provided examples plus any edge cases

```python
from typing import List


class Solution:
    def exampleMethod(self, nums: List[int]) -> int:
        pass

if __name__ == "__main__":
    solution = Solution()
    assert solution.exampleMethod([1, 2, 3]) == 6
    print("All test cases passed!")
```

## README.md Format (per problem)

Each problem folder must contain a `README.md` with this exact structure:

```markdown
# <number>. <Title>

**Link:** <leetcode url> \
**Difficulty:** Easy | Medium | Hard \
**Topics:** Topic1, Topic2

## Description

<problem statement>

## Examples

**Example 1:**

\`\`\`text Input: ... Output: ... \`\`\`

## Constraints

- `constraint 1`
- `constraint 2`
```

## Root README.md Table

Whenever a new problem is added, append a row to the solutions table in the root
`README.md`:

```markdown
| [N](problems/XXXX-problem-name/solution.py) |
[Title](problems/XXXX-problem-name/solution.py) | Easy/Medium/Hard | Topic1,
Topic2 |
```

Rows must be sorted by problem number in ascending order.

## Naming Convention

| Element | Convention                             | Example                    |
| ------- | -------------------------------------- | -------------------------- |
| Folder  | `XXXX-kebab-case`                      | `0042-trapping-rain-water` |
| File    | always `solution.py` / `README.md`     | —                          |
| Class   | always `Solution`                      | —                          |
| Method  | camelCase, matching LeetCode signature | `maxProfit`                |

## CLI — `leet`

All tooling is accessed via the `leet` CLI at the repo root:

```bash
# Scaffold a new problem from its LeetCode URL
python3 leet create:problem https://leetcode.com/problems/two-sum/

# Run tests for all problems
python3 leet test

# Run tests for a specific problem (by number)
python3 leet test 42
```

## tests.json Format

Each problem folder must include a `tests.json` for `python3 leet test`:

```json
{
  "method": "<LeetCode method name>",
  "normalizer": "sort",
  "param_types": ["ListNode", "ListNode"],
  "return_type": "ListNode",
  "cases": [
    {
      "label": "Human-readable description",
      "args": [<positional arg1>, <positional arg2>],
      "expected": <expected return value>
    }
  ]
}
```

- `"label"` is optional but recommended
- `"normalizer"` is optional; applies a transform to both result and expected
  before comparing:
  - `"sort"` — `sorted(result)` (use when output order is non-deterministic,
    e.g. "return in any order")
  - `"sort_nested"` — sort a list of lists (any order at both levels)
  - `"set"` — `frozenset(result)` (unordered, no duplicates)
- `"param_types"` is optional; list of raw LeetCode type strings per argument.
  When present, the runner converts plain-list args to `ListNode`/`TreeNode`
  using `from_list()`. Generated automatically by `leet create:problem`.
- `"return_type"` is optional; raw LeetCode return type. When present, the
  runner calls `.to_list()` on the result before comparing with `expected`.
- `"args"` is always an array of positional arguments matching the method
  signature
