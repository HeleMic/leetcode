from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        area, leftIndex, rightIndex, maxHeight = 0, 0, len(height) - 1, max(height)
        while leftIndex < rightIndex:
            width = rightIndex - leftIndex
            area = max(area, min(height[leftIndex], height[rightIndex]) * width)

            if maxHeight * width <= area:
                break

            if height[leftIndex] < height[rightIndex]:
                currLeftHeight = height[leftIndex]
                leftIndex += 1
                while leftIndex < rightIndex and currLeftHeight > height[leftIndex]:
                    leftIndex += 1
            else:
                currRightHeight = height[rightIndex]
                rightIndex -= 1
                while leftIndex < rightIndex and currRightHeight > height[rightIndex]:
                    rightIndex -= 1

        return area


if __name__ == "__main__":
    import subprocess
    from pathlib import Path

    executablePath = Path(__file__).parent.parent.parent / "leet"
    testNumber = Path(__file__).parent.name.split("-")[0]
    subprocess.run(["python3", executablePath, "test", testNumber])
