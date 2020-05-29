# @Time    : 2020/5/29 9:20
# @Author  : Libuda
# @FileName: analyze.py
# @Software: PyCharm
import numpy as np
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Line, Bar, Page, Pie
from pyecharts.commons.utils import JsCode

# 人口数量excel文件保存路径
POPULATION_EXCEL_PATH = 'Population of India (2020 and historical).xlsx'

# 读取标准数据
DF_STANDARD = pd.read_excel(POPULATION_EXCEL_PATH)
print(DF_STANDARD)
# 自定义pyecharts图形背景颜色js
background_color_js = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#c86589'}, {offset: 1, color: '#06a7ff'}], false)"
)
# 自定义pyecharts图像区域颜色js
area_color_js = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)"
)


def analysis_total():
    """
    分析总人口
    """
    # 1、分析总人口，画人口曲线图
    # 1.1 处理数据
    x_data = DF_STANDARD['Year'][::-1]
    # 将人口单位转换为万
    y_data = DF_STANDARD['Population'].map(lambda x: "%.2f" % (x / 10000))[::-1]
    # y_data = DF_STANDARD['Population'][::-1]
    # 1.2 自定义曲线图
    line = (
        Line(init_opts=opts.InitOpts(bg_color=JsCode(background_color_js)))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="总人口",
            y_axis=y_data,
            is_smooth=True,
            is_symbol_show=True,
            symbol="circle",
            symbol_size=5,
            linestyle_opts=opts.LineStyleOpts(color="#fff"),
            label_opts=opts.LabelOpts(is_show=False, position="top", color="white"),
            itemstyle_opts=opts.ItemStyleOpts(
                color="red", border_color="#fff", border_width=1
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="印度人口变化(万人)",
                pos_bottom="5%",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=16),
            ),
            # x轴相关的选项设置
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=False,
                axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=25,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=False, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            # y轴相关选项设置
            yaxis_opts=opts.AxisOpts(
                type_="value",
                position="left",
                axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(width=0, color="#ffffff1f")
                ),
                axistick_opts=opts.AxisTickOpts(
                    is_show=True,
                    length=15,
                    linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                ),
                splitline_opts=opts.SplitLineOpts(
                    is_show=False, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                ),
            ),
            # 图例配置项相关设置
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    # 3、渲染图像，将多个图像显示在一个html中
    # DraggablePageLayout表示可拖拽
    page = Page(layout=Page.SimplePageLayout)
    page.add(line)
    # page.add(bar)
    page.render('population_total.html')


if __name__ == '__main__':
    analysis_total()
