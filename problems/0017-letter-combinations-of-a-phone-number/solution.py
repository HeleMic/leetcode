from typing import Any


class Solution:
    def letterCombinations(self, digits: str) -> Any:
        digitLettersMap = {
            "2": ["a", "b", "c"],
            "3": ["d", "e", "f"],
            "4": ["g", "h", "i"],
            "5": ["j", "k", "l"],
            "6": ["m", "n", "o"],
            "7": ["p", "q", "r", "s"],
            "8": ["t", "u", "v"],
            "9": ["w", "x", "y", "z"],
        }

        def _recursion(_digits: str, index: int = 0) -> list[str]:
            if index == len(digits) - 1:
                return digitLettersMap[_digits[index]]

            result = set()

            nextValues = _recursion(_digits, index + 1)
            for char in digitLettersMap[_digits[index]]:
                for nextValue in nextValues:
                    result.add("".join(char + nextValue))

            return result

        if len(digits) == 0:
            return []

        result = _recursion(digits)
        return list(result)


if __name__ == "__main__":
    import subprocess
    from pathlib import Path

    executablePath = Path(__file__).parent.parent.parent / "leet"
    testNumber = Path(__file__).parent.name.split("-")[0]
    subprocess.run(["python3", executablePath, "test", testNumber])
