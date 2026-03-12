# LeetCode Solutions

A collection of my solutions to LeetCode problems, organized by problem number.

## Structure

```text
problems/
└── XXXX-problem-name/
    ├── README.md     # problem description
    ├── solution.py   # solution with time & space complexity
    └── tests.json    # test cases for the runner
```

## Solutions

| #                                              | Title                                                        | Difficulty | Topics                       |
| ---------------------------------------------- | ------------------------------------------------------------ | ---------- | ---------------------------- |
| [1](problems/0001-two-sum/solution.py)         | [Two Sum](problems/0001-two-sum/solution.py)                 | Easy       | Array, Hash Table            |
| [2](problems/0002-add-two-numbers/solution.py) | [Add Two Numbers](problems/0002-add-two-numbers/solution.py) | Medium     | Linked List, Math, Recursion |

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
