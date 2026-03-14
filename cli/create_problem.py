"""create:problem — scaffold a new problem directory from a LeetCode URL."""

import json
import re
import ssl
import urllib.request
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

from cli._utils import _die

REPO_ROOT = Path(__file__).parent.parent
PROBLEMS_DIR = REPO_ROOT / "problems"
ROOT_README = REPO_ROOT / "README.md"

GRAPHQL_URL = "https://leetcode.com/graphql"
GRAPHQL_QUERY = """
query ($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId title difficulty
    topicTags { name }
    content exampleTestcaseList metaData
  }
}
"""

TYPE_MAP = {
    "integer": "int",
    "integer[]": "List[int]",
    "integer[][]": "List[List[int]]",
    "string": "str",
    "string[]": "List[str]",
    "string[][]": "List[List[str]]",
    "boolean": "bool",
    "double": "float",
    "long": "int",
    "character": "str",
    "character[]": "List[str]",
    "ListNode": "Optional[ListNode]",
}
COMMON_TYPES = {"ListNode"}


# ── HTML → Markdown ───────────────────────────────────────────────────────────

class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._parts: list[str] = []
        self._in_pre = False

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            self._in_pre = True
            self._parts.append("\n```text\n")
        elif tag in ("p", "li", "ul", "ol"):
            self._parts.append("\n")
        elif tag == "strong" and not self._in_pre:
            self._parts.append("**")
        elif tag == "code" and not self._in_pre:
            self._parts.append("`")

    def handle_endtag(self, tag):
        if tag == "pre":
            self._in_pre = False
            self._parts.append("```")
        elif tag == "strong" and not self._in_pre:
            self._parts.append("**")
        elif tag == "code" and not self._in_pre:
            self._parts.append("`")

    def handle_data(self, data):
        self._parts.append(data)

    def get_text(self) -> str:
        text = "".join(self._parts)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.replace("\xa0", " ").strip()


def _html_to_md(html: str) -> str:
    s = _HTMLStripper()
    s.feed(html)
    return s.get_text()


# ── LeetCode API ──────────────────────────────────────────────────────────────

def _fetch_problem(slug: str) -> dict:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    payload = json.dumps({"query": GRAPHQL_QUERY, "variables": {"titleSlug": slug}}).encode()
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://leetcode.com",
        },
    )
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        data = json.loads(resp.read())
    if "errors" in data:
        raise RuntimeError(f"GraphQL error: {data['errors']}")
    q = data["data"]["question"]
    if q is None:
        raise RuntimeError(f"Problem '{slug}' not found on LeetCode.")
    return q


def _slug_from_url(url: str) -> str:
    url = url.rstrip("/")
    m = re.search(r"leetcode\.com/problems/([^/]+)", url)
    if not m:
        raise ValueError(f"Cannot extract problem slug from URL: {url}")
    return m.group(1)


# ── Type utilities ────────────────────────────────────────────────────────────

def _py_type(lc: str) -> str:
    return TYPE_MAP.get(lc, "Any")


def _parse_metadata(meta_json: str):
    meta = json.loads(meta_json)
    method = meta["name"]
    params = meta.get("params", [])
    ret = _py_type(meta.get("return", {}).get("type", "Any"))
    return method, params, ret


def _build_imports(params, ret_type):
    typing_needed: set[str] = set()
    common_needed: set[str] = set()
    for t in [_py_type(p["type"]) for p in params] + [ret_type]:
        if "List" in t:
            typing_needed.add("List")
        if "Optional" in t:
            typing_needed.add("Optional")
        if "Any" in t:
            typing_needed.add("Any")
        for ct in COMMON_TYPES:
            if ct in t:
                common_needed.add(ct)
    return sorted(typing_needed), sorted(common_needed)


# ── File generators ───────────────────────────────────────────────────────────

def _make_readme(q: dict, slug: str) -> str:
    html = q["content"]
    desc_html = re.split(r'<p><strong class="example">', html)[0]
    description = _html_to_md(desc_html).strip()

    example_blocks = re.findall(r"<pre>(.*?)</pre>", html, re.DOTALL)
    examples_parts = []
    for i, block in enumerate(example_blocks, 1):
        text = re.sub(r"<[^>]+>", "", block).strip()
        lines = [ln.rstrip() for ln in text.splitlines()]
        examples_parts.append(f"**Example {i}:**\n\n```text\n" + "\n".join(lines) + "\n```")

    c_match = re.search(
        r"<p><strong>Constraints:</strong></p>(.*?)(?:<p><strong>|$)", html, re.DOTALL
    )
    if c_match:
        items = re.findall(r"<li>(.*?)</li>", c_match.group(1), re.DOTALL)
        constraints_md = "\n".join(
            f"- `{unescape(re.sub(r'<[^>]+>', '', item)).strip()}`" for item in items
        )
    else:
        constraints_md = ""

    topics = ", ".join(t["name"] for t in q["topicTags"])
    url = f"https://leetcode.com/problems/{slug}/"
    return (
        "\n".join([
            f"# {q['questionId']}. {q['title']}",
            "",
            f"**Link:** <{url}>  ",
            f"**Difficulty:** {q['difficulty']}  ",
            f"**Topics:** {topics}",
            "",
            "## Description",
            "",
            description,
            "",
            "## Examples",
            "",
            "\n\n".join(examples_parts),
            "",
            "## Constraints",
            "",
            constraints_md,
        ])
        + "\n"
    )


def _make_solution(method: str, params: list, ret_type: str) -> str:
    typing_imports, common_imports = _build_imports(params, ret_type)
    param_str = ", ".join(f"{p['name']}: {_py_type(p['type'])}" for p in params)
    lines = []
    if typing_imports:
        lines.append(f"from typing import {', '.join(typing_imports)}")
    if common_imports:
        lines.append(f"from common import {', '.join(common_imports)}")
    if lines:
        lines.append("")
    lines += [
        "",
        "class Solution:",
        f"    def {method}(self, {param_str}) -> {ret_type}:",
        '        """',
        "        Time:  O(?)",
        "        Space: O(?)",
        '        """',
        "        pass",
        "",
        "",
        'if __name__ == "__main__":',
        "    import sys",
        "    from pathlib import Path",
        '    sys.path.append(str(Path(__file__).parent.parent.parent))',
        "    from leet import COMMANDS",
        '    COMMANDS["test"]([Path(__file__).parent.name.split("-")[0]])',
    ]
    return "\n".join(lines) + "\n"


def _make_tests_json(method: str, example_list: list, params: list, ret_type: str) -> str:
    raw_param_types = [p["type"] for p in params]
    py_param_types = [_py_type(t) for t in raw_param_types]
    needs_coerce = any(ct in t for t in py_param_types for ct in COMMON_TYPES)
    needs_serialize = any(ct in ret_type for ct in COMMON_TYPES)

    cases = []
    for i, raw in enumerate(example_list, 1):
        args = []
        for line in raw.strip().split("\n"):
            try:
                args.append(json.loads(line))
            except json.JSONDecodeError:
                args.append(line)
        cases.append({"label": f"Example {i}", "args": args, "expected": None})

    data: dict = {"method": method}
    if needs_coerce:
        data["param_types"] = raw_param_types
    if needs_serialize:
        data["return_type"] = re.search(r"(\w+)$", ret_type).group(1)
    data["cases"] = cases
    return json.dumps(data, indent=2) + "\n"


def _update_root_readme(q: dict, folder_name: str) -> None:
    num = int(q["questionId"])
    path = f"problems/{folder_name}/solution.py"
    topics = ", ".join(t["name"] for t in q["topicTags"])
    new_row = f"| [{num}]({path}) | [{q['title']}]({path}) | {q['difficulty']} | {topics} |"

    lines = ROOT_README.read_text().splitlines()
    insert_at = None
    for i, line in enumerate(lines):
        if re.match(r"\|\s*\[?\d", line):
            row_num = int(re.search(r"\[?(\d+)\]?", line).group(1))
            if row_num == num:
                print(f"  Problem #{num} already in README — skipping.")
                return
            if row_num > num and insert_at is None:
                insert_at = i
    if insert_at is None:
        for i in range(len(lines) - 1, -1, -1):
            if re.match(r"\|\s*\[?\d", lines[i]):
                insert_at = i + 1
                break
    if insert_at is None:
        print("  WARNING: Could not locate table in README — skipping.")
        return
    lines.insert(insert_at, new_row)
    ROOT_README.write_text("\n".join(lines) + "\n")
    print("  Updated README.md")


# ── Entry point ───────────────────────────────────────────────────────────────

def run(args: list[str]) -> None:
    if not args:
        _die("Usage: python3 leet create:problem <leetcode-url>")

    slug = _slug_from_url(args[0])
    print(f"Fetching '{slug}' from LeetCode...")
    q = _fetch_problem(slug)

    num = q["questionId"].zfill(4)
    title_kebab = re.sub(r"[^a-z0-9]+", "-", q["title"].lower()).strip("-")
    folder_name = f"{num}-{title_kebab}"
    problem_dir = PROBLEMS_DIR / folder_name

    if problem_dir.exists():
        _die(f"Directory problems/{folder_name} already exists.")

    problem_dir.mkdir(parents=True)
    print(f"  Created problems/{folder_name}/")

    method, params, ret_type = _parse_metadata(q["metaData"])

    (problem_dir / "README.md").write_text(_make_readme(q, slug))
    print("  Created README.md")

    (problem_dir / "solution.py").write_text(_make_solution(method, params, ret_type))
    print(f"  Created solution.py  (method: {method})")

    (problem_dir / "tests.json").write_text(
        _make_tests_json(method, q["exampleTestcaseList"], params, ret_type)
    )
    n = len(q["exampleTestcaseList"])
    print(f"  Created tests.json   ({n} example case{'s' if n != 1 else ''} — fill in 'expected')")

    _update_root_readme(q, folder_name)

    print(f"\nDone! Next steps:")
    print(f"  1. Fill in 'expected' values in  problems/{folder_name}/tests.json")
    print(f"  2. Solve the problem in          problems/{folder_name}/solution.py")
    print(f"  3. python3 leet test {int(q['questionId'])}")
