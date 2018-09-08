#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/4


def findMedianSortedArrays(nums1, nums2):#时间复杂度不符合要求
    """
    :type nums1: List[int]
    :type nums2: List[int]
    :rtype: float
    """
    nums1 +=nums2
    nums1.sort()
    l = len(nums1)
    if l%2 == 0:
        return (nums1[l//2-1] +nums1[l//2])/2.0
    else:
        return nums1[l//2]

def median(A, B):
    m, n = len(A), len(B)
    if m > n:
        A, B, m, n = B, A, n, m
    if n == 0:
        raise ValueError

    imin, imax, half_len = 0, m, (m + n + 1) / 2
    while imin <= imax:
        i = int((imin + imax) / 2)
        j = int(half_len - i)
        if i < m and B[j-1] > A[i]:
            # i is too small, must increase it
            imin = i + 1
        elif i > 0 and A[i-1] > B[j]:
            # i is too big, must decrease it
            imax = i - 1
        else:
            # i is perfect

            if i == 0: max_of_left = B[j-1]
            elif j == 0: max_of_left = A[i-1]
            else: max_of_left = max(A[i-1], B[j-1])

            if (m + n) % 2 == 1:
                return max_of_left

            if i == m: min_of_right = B[j]
            elif j == n: min_of_right = A[i]
            else: min_of_right = min(A[i], B[j])

            return (max_of_left + min_of_right) / 2.0


res=median([1,2,3,3,8,9,10],[2,3,4])
print(res)