from typing import Optional
from common import ListNode


class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:

        def _recursive(_l1: Optional[ListNode], _l2: Optional[ListNode], _carry: int = 0) -> Optional[ListNode]:
            if _l1 is None and _l2 is None:
                return None if _carry == 0 else ListNode(_carry)

            n1 = _l1.val if _l1 else 0
            n2 = _l2.val if _l2 else 0
            res = n1 + n2 + _carry
            return ListNode(
                res - 10 if res > 9 else res,
                _recursive(_l1.next if _l1 else None, _l2.next if _l2 else None, 1 if res > 9 else 0)
            )

        return _recursive(l1, l2)


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from cli import COMMANDS
    COMMANDS["test"]([Path(__file__).parent.name.split("-")[0]])

