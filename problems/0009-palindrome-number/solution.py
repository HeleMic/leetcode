class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False

        x2, num = x, 0
        while x2 > 0:
            num = (num * 10) + (x2 % 10)
            x2 //= 10

        return x == num


if __name__ == "__main__":
    import subprocess
    from pathlib import Path

    executablePath = Path(__file__).parent.parent.parent / "leet"
    testNumber = Path(__file__).parent.name.split("-")[0]
    subprocess.run(["python3", executablePath, "test", testNumber])
