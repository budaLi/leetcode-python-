#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/6
# 特殊情况 {}【】（） 不能从中间判断
# 我们可以判断每一个和他后面的是否匹配
def isValid(s):
        if s is None: return False

        x = ['[','(','{']
        y = ["]",")","}"]
        z = ["()","[]","{}"]

        res = []
        for i in s:
            if i in x:
                res.append(i) # 入栈
            elif i in y:
                # 如果收到一个右括号，但是res中无左括号，直接返回False
                if res == []:
                    return False
                else:
                    temp = res.pop(-1) + i
                    # 其余情况，出栈一个左括号，判断左括号+右括号是否有效
                    if temp not in z:
                        return False
        # 如果所有括号对都满足，但是res还有左括号，返回False
        if len(res) != 0:
            return False
        return True
lis="()[]{}"
res=isValid(lis)
print(res)
