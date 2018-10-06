#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/6
from __future__ import unicode_literals
from pyecharts import Bar

attr = [ ' Jan ',' Feb ',' Mar ',' Apr ',' May ',' Jun ',' Jul ',' Aug ',' Sep ',' Oct ',' Nov ',' Dec ' ]
V1 = [ 2.0,4.9,7.0,23.2,25.6,76.7,135.6,162.2,32.6,20.0,6.4,3.3 ]
V2 = [ 2.6,5.9,9.0,26.4,28.7,70.7,175.6,182.2,48.7,18.8,6.0,2.3 ]
bar = Bar('条形图','降水和蒸发一年')
bar.add(' precipitation ',attr,V1,mark_line = [ ' average ' ],mark_point = [ ' max ',' min ' ])
bar.add('蒸发',attr,V2,mark_line = [ '平均' ],mark_point = [ '最大','最小' ])
bar.render()