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
    solution = Solution()
    assert solution.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert solution.twoSum([3, 2, 4], 6) == [1, 2]
    assert solution.twoSum([3, 3], 6) == [0, 1]
    print("All test cases passed!")
