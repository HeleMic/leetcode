from typing import List
from math import ceil


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        length = len(nums1) + len(nums2)
        if length == 0:
            return 0

        merged = []
        index, index1, index2, stop = 0, 0, 0, length // 2 + 1

        while index1 < len(nums1) and index2 < len(nums2) and index < stop:
            index += 1
            if nums1[index1] < nums2[index2]:
                merged.append(nums1[index1])
                index1 += 1

            elif nums2[index2] < nums1[index1]:
                merged.append(nums2[index2])
                index2 += 1

            else:
                merged.append(nums1[index1])
                merged.append(nums2[index2])
                index += 1
                index1 += 1
                index2 += 1

        merged.extend(nums1[index1:])
        merged.extend(nums2[index2:])

        middle = len(merged) // 2

        values = [merged[middle - 1], merged[middle]] if len(merged) % 2 == 0 else [merged[middle]]
        return sum(values) / len(values)



if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from cli import COMMANDS
    COMMANDS["test"]([Path(__file__).parent.name.split("-")[0]])

