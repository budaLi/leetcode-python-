#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/7
def findWords(words):
    """
    :type words: List[str]
    :rtype: List[str]
    """
    one={'q','Q','w','W','e','E','r','R','t','T','y','Y','u','U','i','I','O','o','p','P'}
    two={'a','A','s','S','d','D','f','F','g','G','h','H','j','J','k','K','l','L'}
    three={'z','Z','x','X','c','C','v','V','b','B','n','N','m','M'}
    res=[]
    for word in words:
        if all(word[i] in one for i in range(len(word))) or all(word[i] in two for i in range(len(word))) or all(word[i] in three for i in range(len(word))):
            res.append(word)

    return res

res=findWords(["Hello", "Alaska", "Dad", "Peace"])
print(res)