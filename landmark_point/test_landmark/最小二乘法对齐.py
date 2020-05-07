# @Time    : 2020/5/7 15:58
# @Author  : Libuda
# @FileName: 最小二乘法对齐.py
# @Software: PyCharm
import numpy as np
import cv2

from numpy.linalg import inv, norm, lstsq
from numpy.linalg import matrix_rank as rank


def findNonreflectiveSimilarity(uv, xy, K=2):
    M = xy.shape[0]
    x = xy[:, 0].reshape((-1, 1))  # use reshape to keep a column vector
    y = xy[:, 1].reshape((-1, 1))  # use reshape to keep a column vector

    tmp1 = np.hstack((x, y, np.ones((M, 1)), np.zeros((M, 1))))
    tmp2 = np.hstack((y, -x, np.zeros((M, 1)), np.ones((M, 1))))
    X = np.vstack((tmp1, tmp2))

    u = uv[:, 0].reshape((-1, 1))  # use reshape to keep a column vector
    v = uv[:, 1].reshape((-1, 1))  # use reshape to keep a column vector
    U = np.vstack((u, v))

    # We know that X * r = U
    if rank(X) >= 2 * K:
        r, _, _, _ = lstsq(X, U)
        r = np.squeeze(r)
    else:
        raise Exception('cp2tform:twoUniquePointsReq')

    sc = r[0]
    ss = r[1]
    tx = r[2]
    ty = r[3]

    Tinv = np.array([
        [sc, -ss, 0],
        [ss, sc, 0],
        [tx, ty, 1]
    ])

    T = inv(Tinv)

    T[:, 2] = np.array([0, 0, 1])

    T = T[:, 0:2].T

    return T


img_path = "6_40_Gymnastics_Gymnastics_40_5_0.png"
save_path = "test1.png"

detect_landmark_txt = "caffe_list.txt"
img = cv2.imread(img_path)

h, w, _ = img.shape

with open(detect_landmark_txt) as f:
    lines = f.readlines()
    image_indx = 594
    new_landmakr = []
    for i in range(image_indx, len(lines), 99):
        landmark = lines[i + 1:i + 99]
        for ld in landmark:
            x, y = ld.strip().split()
            x, y = float(x) * 112.0, float(y) * 112.0
            new_landmakr.append((x, y))
        break
    new_landmakr = np.asarray(new_landmakr, dtype=np.float32)
landmark = np.asarray(new_landmakr, dtype=np.float32).reshape(98, 2)
# 98点对应5点
pupil_left = landmark[96]
pupil_right = landmark[97]

gt_points_new = np.zeros((5, 2))
gt_points_new[0] = pupil_left
gt_points_new[1] = pupil_right
gt_points_new[2] = landmark[54]
gt_points_new[3] = landmark[76]
gt_points_new[4] = landmark[82]

landmark = np.asarray([[166.7, 180.0],
                       [233.3, 180.0],
                       [179.9, 235.1],
                       [174.4, 296.2],
                       [236.2, 297.3]])

REFERENCE_FACIAL_POINTS = np.array([
    [30.29459953, 51.69630051],
    [65.53179932, 51.50139999],
    [48.02519989, 71.73660278],
    [33.54930115, 92.3655014],
    [62.72990036, 92.20410156]
], np.float32)
# 读取标签信息，将原图对齐保存
img = cv2.imread(img_path)
similar_trans_matrix = findNonreflectiveSimilarity(landmark, REFERENCE_FACIAL_POINTS)

aligned_face = cv2.warpAffine(img.copy(), similar_trans_matrix, (112, 112))
# aligned_face = cv2.cvtColor(aligned_face, cv2.COLOR_RGB2BGR)

cv2.imwrite("sasa.png", aligned_face)
