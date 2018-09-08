#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/4
import copy
def checkPossibility(nums):
    """
    :type nums: List[int]
    :rtype: bool
    """
    num1=copy.deepcopy(nums)
    return men1(nums) or men2(num1)

def men1(nums):
    print('n1')
    flag=True
    for i in range(len(nums)-1):
        if nums[i]>nums[i+1]:
            if flag==True:
                nums[i+1]=nums[i]
                flag=False
            else:
                print('false')
                return flag
    print(2)
    return True


def men2(nums):
    print('m2')
    flag=True
    for i in range(len(nums)-1):
        print(nums[i])
        if nums[i]>nums[i+1]:
            if flag==True:
                print(nums[i],nums[i+1])
                nums[i]=nums[i+1]
                flag=False
                if i==0:
                    continue
                elif i-1>=0 and nums[i-1]<=nums[i]:
                    print(nums[i-1],nums[i])
                    continue
                else:
                    return False
            else:
                print('false')
                return flag
    return True

res=checkPossibility([1,5,4,6,7,10,8,9])
print(res)
