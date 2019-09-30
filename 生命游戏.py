# @Time    : 2019/9/30 11:26
# @Author  : Libuda
# @FileName: 生命游戏.py
# @Software: PyCharm
class Solution(object):
    def gameOfLife(self, board):
        """
        :type board: List[List[int]]
        :rtype: None Do not return anything, modify board in-place instead.
        """
        import copy
        m = len(board)
        n = len(board[0])
        res = copy.deepcopy(board)
        print(board)
        for i in range(m):
            for j in range(n):
                count = 0
                if i - 1 >= 0 and j - 1 >= 0:  # 左上
                    count += board[i - 1][j - 1]
                if i - 1 >= 0:  # 上
                    count += board[i - 1][j]
                if i - 1 >= 0 and j + 1 < n:
                    count += board[i - 1][j + 1]
                if j - 1 >= 0:
                    count += board[i][j - 1]
                if j + 1 < n:
                    count += board[i][j + 1]
                if i + 1 < m and j - 1 >= 0:
                    count += board[i + 1][j - 1]
                if i + 1 < m:
                    count += board[i + 1][j]
                if i + 1 < m and j + 1 < n:
                    count += board[i + 1][j + 1]
                if count < 2:
                    res[i][j] = 0
                elif count == 3:
                    res[i][j] = 1
                elif count > 3:
                    res[i][j] = 0

        return res


if __name__ == "__main__":
    S = Solution()
    s = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ]
    res = S.gameOfLife(s)
    print(res)
