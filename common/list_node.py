from __future__ import annotations
from typing import List, Optional


class ListNode:
    """Singly-linked list node used by LeetCode linked-list problems."""

    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next

    # ── Convenience helpers (not part of the LeetCode API) ──────────────────

    def to_list(self) -> List[int]:
        """Collect all node values into a plain Python list."""
        values: List[int] = []
        node: Optional[ListNode] = self
        while node is not None:
            values.append(node.val)
            node = node.next
        return values

    @classmethod
    def from_list(cls, values: List[int]) -> Optional[ListNode]:
        """Build a linked list from a plain Python list (head first)."""
        head: Optional[ListNode] = None
        for value in reversed(values):
            head = cls(value, head)
        return head

    def __repr__(self) -> str:
        return f"ListNode({self.to_list()})"
