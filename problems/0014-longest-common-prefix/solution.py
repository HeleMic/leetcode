from typing import List


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        maxLength = min(len(string) for string in strs)
        if maxLength == 0:
            return ""

        result = ""
        for i in range(maxLength):
            for j in range(1, len(strs)):
                if strs[j - 1][i] != strs[j][i]:
                    return result
            result += strs[0][i]

        return result


if __name__ == "__main__":
    import subprocess
    from pathlib import Path

    executablePath = Path(__file__).parent.parent.parent / "leet"
    testNumber = Path(__file__).parent.name.split("-")[0]
    subprocess.run(["python3", executablePath, "test", testNumber])
