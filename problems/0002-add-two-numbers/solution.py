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
    solution = Solution()
    solution1 = solution.addTwoNumbers(ListNode.from_list([2, 4, 3]), ListNode.from_list([5, 6, 4]))
    solution2 = solution.addTwoNumbers(ListNode.from_list([0]), ListNode.from_list([0]))
    solution3 = solution.addTwoNumbers(ListNode.from_list([9, 9, 9, 9, 9, 9, 9]), ListNode.from_list([9, 9, 9, 9]))
    assert solution1 and solution1.to_list() == [7, 0, 8]
    assert solution2 and solution2.to_list() == [0]
    assert solution3 and solution3.to_list() == [8, 9, 9, 9, 0, 0, 0, 1]
    print("All test cases passed!")
