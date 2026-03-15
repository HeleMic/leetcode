# Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value
# to go outside the signed 32-bit integer range [-231, 231 - 1], then return 0.


class Solution:
    def reverse(self, x: int) -> int:
        mul = 1
        if x < 0:
            mul = -1
            x = abs(x)

        reversedNumber = 0
        while x > 0:
            if reversedNumber > 214748364:
                return 0
            reversedNumber = (reversedNumber * 10) + (x % 10)
            x //= 10

        return reversedNumber * mul


if __name__ == "__main__":
    import subprocess
    from pathlib import Path

    executablePath = Path(__file__).parent.parent.parent / "leet"
    testNumber = Path(__file__).parent.name.split("-")[0]
    subprocess.run(["python3", executablePath, "test", testNumber])
