#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/7
def maxSubArray(num_list):  #时间复杂度n
    max_value=-2**32     #我们应该从保留第一个数出发 所以定义一个很小的负数
    length=len(num_list)
    tem=0
    for i in range(length):
        tem=max(tem+num_list[i],num_list[i])
        max_value=max(max_value,tem)
    return max_value

res=maxSubArray([-2,1,-3,1,2,4])
print(res)