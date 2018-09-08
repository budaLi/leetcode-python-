#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/13
#未完成
def possibleBipartition( N, dislikes):
    A=[i for i in range(1,N+1)]
    B=[]
    for i in range(1,N+1):
        for j in range(1,N+1):
            if i<j:
                B.append([i,j])
    print(B)
    for one in dislikes:
        if one in B:
            B.pop(B.index(one))
    print(B)
    for one in B:
        A=list(set(A).difference(one))
        print(A)
        if list(set(A).difference(one)) in B:
            print(list(set(A).difference(one)))
            return True
    if len(A)==1:
        return True
    return False
S=possibleBipartition(5,
[[1,2],[2,3],[3,4],[4,5],[1,5]])
print(S)

