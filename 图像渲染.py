#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/27
def floodFill(self, image, sr, sc, newColor):
    ogColor = image[sr][sc]
    image[sr][sc] = newColor
    mark =[[sr,sc]]             # 用于标记去过的点
    return self.dfs(image, sr, sc, ogColor, newColor, mark)

def dfs(self, image, i, j, ogColor, newColor, mark):
    h = len(image)
    w = len(image[0])

    direction = [[1,0], [0,1], [-1,0], [0,-1]]
    for d in direction:
        x = i + d[0]
        y = j + d[1]
        if x>=0 and x<h and y>=0 and y<w and image[x][y]==ogColor and [x,y] not in mark:    # 最后的条件防止回退陷入死循环
            mark += [[x,y]]     # 新加入当前的点
            image[x][y] = newColor
            image = self.dfs( image, x, y, ogColor, newColor, mark )

    return image