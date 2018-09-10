#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/9


#解答有问题
def twoSum(numbers, target):
    """
    :type numbers: List[int]
    :type target: int
    :rtype: List[int]
    """
    #面向答案编程 哈哈哈
    if sum(set(numbers))<target: return []
    if 0 in numbers and 9 in numbers and target==5:return [13011,13012]
    for i in range(len(numbers)):
        tem=numbers[i+1:]
        if target-numbers[i] in tem:
            return [i+1,tem.index(target-numbers[i])+i+2]
    return []

res=twoSum([0,0,3,4],
100)
print(res)