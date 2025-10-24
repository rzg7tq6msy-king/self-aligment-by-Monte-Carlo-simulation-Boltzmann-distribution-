# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 09:36:24 2025

@author: 25015
"""

from shapely.geometry import MultiPolygon# 导入 MultiPolygon 类，用于识别和处理多多边形对象

def energy(poly_list1, poly_list2):
    # 如果不是列表，先包装成列表
    if not isinstance(poly_list1, list):
        if isinstance(poly_list1, MultiPolygon):
            poly_list1 = list(poly_list1.geoms)
        else:
            poly_list1 = [poly_list1]

    if not isinstance(poly_list2, list):
        if isinstance(poly_list2, MultiPolygon):
            poly_list2 = list(poly_list2.geoms)
        else:
            poly_list2 = [poly_list2]

    total_overlap = 0
    for p1 in poly_list1:
        for p2 in poly_list2:
            total_overlap += p1.intersection(p2).area

    return -total_overlap  # 重叠越大，能量越低
