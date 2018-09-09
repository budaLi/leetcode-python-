#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/9
def twoSum(numbers, target):
    """
    :type numbers: List[int]
    :type target: int
    :rtype: List[int]
    """
    if sum(set(numbers))<target: return []
    for i in range(len(numbers)):
        tem=numbers[i+1:]
        if target-numbers[i] in tem:
            print(target-numbers[i])
            return [i+1,tem.index(target-numbers[i])+i+2]
    return []

res=twoSum([0,0,3,4],
100)
print(res)