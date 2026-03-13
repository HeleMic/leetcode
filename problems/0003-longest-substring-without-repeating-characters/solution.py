
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        values = {}
        w_left, w_right, counter = 0, 0, 0

        while w_right < len(s):
            char = s[w_right]
            if char in values:
                counter = max(counter, w_right - w_left)
                values.pop(s[w_left])
                w_left += 1
                continue
            w_right += 1
            values[char] = True

        return max(counter, w_right - w_left)


if __name__ == "__main__":
    test_cases = (
        ("abcabcbb", 3),
        ("bbbbb", 1),
        ("pwwkew", 3),
    )

    solution = Solution()

    for tc_index, tc in enumerate(test_cases):
        print("====================================================================================")
        print(f"Running test case #{tc_index + 1} with value \"{tc[0]}\" and expected output \"{tc[1]}\"")
        print("====================================================================================")
        print()
        assert solution.lengthOfLongestSubstring(tc[0]) == tc[1]
        print()

    print("All test cases passed!")
