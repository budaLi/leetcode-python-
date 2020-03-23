# @Time    : 2020/3/10 11:42
# @Author  : Libuda
# @FileName: tes.py
# @Software: PyCharm
tem = """ModelNo:890638376,
KernelVer:3.6.3.0,
AppVer:3.6.109.1,
ModelName:FNC-C3-irbow-ZWH,
2002:1,
2004:0,
2005:0,
2007:1,
2008:1,
2010:2,
2011:2,
2012:1,
2013:1,
2014:0,
2033:1,
getProductConfig:OK,"""
tem_dict = {}
tem_lis = tem.split("\n")
print(tem_lis)
for one in tem_lis:
    tem_dict.update({key, words} for key, words in one.split(":"))
print(tem_dict)
