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

| #                                      | Title                                        | Difficulty | Topics            |
| -------------------------------------- | -------------------------------------------- | ---------- | ----------------- |
| [1](problems/0001-two-sum/solution.py) | [Two Sum](problems/0001-two-sum/solution.py) | Easy       | Array, Hash Table |

## Running Tests

```bash
# Run all tests
python3 run_tests.py

# Run tests for a specific problem (by number)
python3 run_tests.py 1
python3 run_tests.py 0042
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

- `"label"` _(optional)_ — human-readable name shown in the test output
  (defaults to `"Case N"`)
- `"args"` — positional arguments matching the method signature exactly
