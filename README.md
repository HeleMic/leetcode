# LeetCode Solutions

A collection of my solutions to LeetCode problems, organized by problem number.

## Solutions

| #                                                                             | Title                                                                                                                      | Difficulty | Topics                                   |
| ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------- |
| [1](problems/0001-two-sum/solution.py)                                        | [Two Sum](problems/0001-two-sum/solution.py)                                                                               | Easy       | Array, Hash Table                        |
| [2](problems/0002-add-two-numbers/solution.py)                                | [Add Two Numbers](problems/0002-add-two-numbers/solution.py)                                                               | Medium     | Linked List, Math, Recursion             |
| [3](problems/0003-longest-substring-without-repeating-characters/solution.py) | [Longest Substring Without Repeating Characters](problems/0003-longest-substring-without-repeating-characters/solution.py) | Medium     | Hash Table, String, Sliding Window       |
| [4](problems/0004-median-of-two-sorted-arrays/solution.py)                    | [Median of Two Sorted Arrays](problems/0004-median-of-two-sorted-arrays/solution.py)                                       | Hard       | Array, Binary Search, Divide and Conquer |
| [7](problems/0007-reverse-integer/solution.py)                                | [Reverse Integer](problems/0007-reverse-integer/solution.py)                                                               | Medium     | Math                                     |
| [9](problems/0009-palindrome-number/solution.py)                              | [Palindrome Number](problems/0009-palindrome-number/solution.py)                                                           | Easy       | Math                                     |
| [11](problems/0011-container-with-most-water/solution.py)                     | [Container With Most Water](problems/0011-container-with-most-water/solution.py)                                           | Medium     | Array, Two Pointers, Greedy              |
| [14](problems/0014-longest-common-prefix/solution.py)                         | [Longest Common Prefix](problems/0014-longest-common-prefix/solution.py)                                                   | Easy       | Array, String, Trie                      |

## Structure

```text
common/               # shared data structures (ListNode, TreeNode)
problems/
└── XXXX-problem-name/
    ├── README.md     # problem description
    ├── solution.py   # solution with time & space complexity
    └── tests.json    # test cases for the runner
```

## Shared Data Structures

The `common/` package provides implementations for LeetCode-specific data
structures like `ListNode` and `TreeNode`.

### Usage in Solutions

When solving a problem that uses these structures (e.g., Linked Lists or Trees),
import them from the `common` package:

```python
from common import ListNode        # or TreeNode
```

These classes include helper methods:

- `from_list(values: list)`: Creates a linked list or binary tree from a list
- `to_list()`: Serializes the structure back into a list

The repository is configured to make `common` importable anywhere if you have
installed it in editable mode via `pip install -e .`.

## Adding a New Problem

```bash
python3 leet create:problem https://leetcode.com/problems/two-sum/
```

This will automatically:

- Create `problems/XXXX-problem-name/` with `README.md`, `solution.py`, and
  `tests.json`
- Populate the README with the problem description, examples, and constraints
- Populate `tests.json` with the official example inputs (fill in `expected`
  values manually)
- Add the problem to the table above

After running, fill in the `expected` values in `tests.json` and solve the
problem in `solution.py`.

## Running Tests

```bash
# Run all tests
python3 leet test

# Run tests for a specific problem (by number)
python3 leet test 1
python3 leet test 42
```

## Adding Test Cases

Each problem folder contains a `tests.json` file. Add new cases to the `cases`
array:

```json
{
  "method": "twoSum",
  "normalizer": "sort",
  "cases": [
    {
      "label": "Example 1",
      "args": [[2, 7, 11, 15], 9],
      "expected": [0, 1]
    }
  ]
}
```

**Fields:**

- `"method"` — name of the method to call on the `Solution` class
- `"normalizer"` _(optional)_ — transformation applied to both result and
  expected before comparing. Use this when the problem allows multiple valid
  outputs (e.g. _"return the answer in any order"_):

  | Value           | Behaviour                                               |
  | --------------- | ------------------------------------------------------- |
  | `"sort"`        | `sorted(result)` — for lists where order doesn't matter |
  | `"sort_nested"` | sort a list of lists at both levels                     |
  | `"set"`         | `frozenset(result)` — unordered, no duplicates          |

- `"param_types"` _(optional)_ — list of raw LeetCode type strings (e.g.
  `["ListNode", "ListNode"]`). When present, the runner converts each `args`
  value from a plain list to the appropriate object (using
  `ListNode.from_list()` or `TreeNode.from_list()`). Generated automatically by
  `leet create:problem` for problems that use linked-list or tree nodes.
- `"return_type"` _(optional)_ — raw LeetCode return type (e.g. `"ListNode"`).
  When present, the runner serializes the method's return value back to a plain
  list before comparing with `expected`.
- `"label"` _(optional)_ — human-readable name shown in the test output
  (defaults to `"Case N"`)
- `"args"` — positional arguments matching the method signature exactly
