#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/1
dic={'2':['a','b','c'],'3':['d','e','f'],
     '4':['g','h','i'],'5':['j','k''l'],
     '6':['m','n','o'],'7':['p','q','r','s'],
     '8':['t','u','v'],'9':['w','x','y','z']
     }
def letterCombinations(digits):
    """
    :type digits: str
    :rtype: List[str]
    """
    # 存储结果的数组
    ret_str = []
    if len(digits) == 0: return []
    # 递归出口，当递归到最后一个数的时候result拿到结果进行for循环遍历
    if len(digits) == 1:
        return dic[digits]
    # 递归调用
    result =letterCombinations(digits[1:])
    # result是一个数组列表，遍历后字符串操作，加入列表
    for r in result:
        for j in dic[digits[0]]:
            ret_str.append(j + r)
    return ret_str



res=letterCombinations('234')
print(res)