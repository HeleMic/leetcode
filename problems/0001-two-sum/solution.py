from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        values_map = {}
        for index in range(len(nums)):
            diff = target - nums[index]
            if diff in values_map:
                return [index, values_map[diff]]
            values_map[nums[index]] = index
        return []

if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from cli import COMMANDS
    COMMANDS["test"]([Path(__file__).parent.name.split("-")[0]])

