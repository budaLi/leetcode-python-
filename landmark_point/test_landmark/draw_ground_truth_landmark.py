# @Time    : 2020/5/7 10:43
# @Author  : Libuda
# @FileName: draw_ground_truth_landmark.py
# @Software: PyCharm

# 分辨list_98pt_rect_attr_test.txt中关键点位置信息

import numpy as np
import cv2

img_path = "37_Soccer_soccer_ball_37_45.jpg"
ground_truth_landmark_txt = "list_98pt_rect_attr_test.txt"
img = cv2.imread(img_path)
h, w, _ = img.shape

with open(ground_truth_landmark_txt) as f:
    line = f.readline()
    line = line.strip().split()
    path = line[-1]
    landmark = line[0:196]
    box = line[196:200]
    attribute = line[200:206]

# x1, y1, w, h = np.asarray(box,dtype=np.int32)
# zz = np.asarray((x1+w,y1+h))
# xy = np.asarray((x1,y1))
# # 人脸框 [w,h]
# wh = zz - xy
# center = (xy + wh / 2).astype(np.int32)
#
# # 选取最大值作为人脸框
# boxsize = int(np.max(wh))
# xy = center - boxsize // 2
# x1, y1 = xy
# x2, y2 = xy + boxsize

x1, y1, x2, y2 = list(map(int, box))
cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
for i in range(98):
    lx, ly = float(landmark[i * 2]), float(landmark[i * 2 + 1])
    lx, ly = int(lx), int(ly)
    cv2.circle(img, (lx, ly), 1, (0, 255, 255), 1)

cv2.imwrite("1.jpg", img)
