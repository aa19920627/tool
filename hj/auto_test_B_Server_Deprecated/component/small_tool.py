'''
@Author：洪建
@Date：2022/1/26 17:16
一些工具方法
'''


# 处理sqlite查询出来的数据，转换成list格式
def deal_select_data(select_list):
    area_list = []
    for i in select_list:
        area_list.append(i[0])
    list_new = list(set(area_list))
    list_new.sort(key=area_list.index)

    return  list_new
