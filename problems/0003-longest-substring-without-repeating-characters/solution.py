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
    import subprocess
    from pathlib import Path

    executablePath = Path(__file__).parent.parent.parent / "leet"
    testNumber = Path(__file__).parent.name.split("-")[0]
    subprocess.run(["python3", executablePath, "test", testNumber])
