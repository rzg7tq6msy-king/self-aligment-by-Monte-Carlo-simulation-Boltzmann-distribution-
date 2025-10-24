# -*- coding: utf-8 -*-
"""
Created on Sat Sep  6 15:02:19 2025

@author: 25015
"""
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely import affinity
import matplotlib.pyplot as plt
from shapely.ops import unary_union

#S=2937
def truncated_ring_segment(r_outer, r_inner, start_angle, end_angle, n_points=50):
    angles = np.linspace(np.radians(start_angle), np.radians(end_angle), n_points)
    outer_x = r_outer * np.cos(angles)
    outer_y = r_outer * np.sin(angles)
    
    if r_inner > 0:
        inner_x = r_inner * np.cos(angles[::-1])
        inner_y = r_inner * np.sin(angles[::-1])
        x = np.concatenate([outer_x, inner_x])
        y = np.concatenate([outer_y, inner_y])
    else:
        x = outer_x
        y = outer_y
    
    return Polygon(np.column_stack([x, y]))

# -------------------- 四段截断圆环 ---------------------
def generate_truncated_ring_L(N, r_outer=77.5, r_inner=62.5):
    angle_ranges = [
        (25, 65),
        (115, 155),
        (205, 245),
        (295, 335),
    ]
    grid = [truncated_ring_segment(r_outer, r_inner, start, end) for start, end in angle_ranges]
    return unary_union(grid)  # 返回一个列表，每个元素是Polygon

# -------------------- 四段截断圆环3 ---------------------
def generate_truncated_ring_S(N, r_outer=30.5, r_inner=0):
    grid = truncated_ring_segment(r_outer, r_inner, 0, 360)
    return unary_union(grid)

# -------------------- 四段截断圆环 ---------------------
def generate_truncated_ring_M4(N, r_outer=58, r_inner=35.5):
    angle_ranges = [
            (25, 65),
            (115, 155),
            (205, 245),
            (295, 335),
    ]
    grid = [truncated_ring_segment(r_outer, r_inner, start, end) for start, end in angle_ranges]
    return unary_union(grid)

# -------------------- 四段截断圆环(内径贴外径) ---------------------
def generate_truncated_ring_M4_2(N, r_outer=62.5, r_inner=42.5):
    angle_ranges = [
        (25, 65),
        (115, 155),
        (205, 245),
        (295, 335),
    ]    
    grid = [truncated_ring_segment(r_outer, r_inner, start, end) for start, end in angle_ranges]
    return unary_union(grid)


# ----------------------- 三段截断圆环 ------------------------
def generate_truncated_ring_M3(N, r_outer=57.5, r_inner=35.5):
    angle_ranges = [
        (62.5, 117.5),
        (182.5, 237.5),
        (302.5, 357.5),
    ]
    grid = [truncated_ring_segment(r_outer, r_inner, start, end) for start, end in angle_ranges]
    return unary_union(grid)



# -------------------- 两段截断圆环 ---------------------
def generate_truncated_ring_M2(N, r_outer=57, r_inner=35.5):
    angle_ranges = [
        (47.5, 132.5),
        (227.5,312.5)
    ]   
    grid = [truncated_ring_segment(r_outer, r_inner, start, end) for start, end in angle_ranges]
    return unary_union(grid)

# -------------------- 一段截断圆环 ---------------------
def generate_truncated_ring_M1(N, r_outer=57, r_inner=35.5):
    angle_ranges = [
        (5, 175),
    ]
    grid = [truncated_ring_segment(r_outer, r_inner, start, end) for start, end in angle_ranges]
    return unary_union(grid)

# -------------------- 马蹄 ---------------------

def generate_truncated_ring_MU(N, r_outer=54, r_inner=39):
   # 分成两段：左侧(150,360)，右侧(0,30)
    angle_ranges = [
        (0, 30),
        (150,360)
     ]
    grid = [truncated_ring_segment(r_outer, r_inner, start, end) for start, end in angle_ranges]
    return unary_union(grid)

# 测试1

N = 169
grid1 = generate_truncated_ring_L(N)
grid2 = generate_truncated_ring_M4(N)
grid3 = generate_truncated_ring_S(N)

from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal')
ax.set_facecolor('white')

# 给每个芯片颜色
colors = ['pink', 'lightgreen', 'skyblue']
all_grids = [grid1, grid2, grid3]
alphas = [0.7, 0.1, 0.1]  # 分别对应 grid1、grid2、grid3 的透明度

for polygons, color in zip(all_grids, colors):
    patches = []
    # 如果是单个 Polygon
    if isinstance(polygons, Polygon):
        patches.append(MplPolygon(np.array(polygons.exterior.coords), closed=True))
    # 如果是 MultiPolygon
    elif isinstance(polygons, MultiPolygon):
        for p in polygons.geoms:
            patches.append(MplPolygon(np.array(p.exterior.coords), closed=True))
    # 如果是列表（像 L、MU 那样）
    elif isinstance(polygons, list):
        for p in polygons:
            if isinstance(p, Polygon):
                patches.append(MplPolygon(np.array(p.exterior.coords), closed=True))
            elif isinstance(p, MultiPolygon):
                for sub in p.geoms:
                    patches.append(MplPolygon(np.array(sub.exterior.coords), closed=True))

    collection = PatchCollection(patches, facecolor=color, edgecolor='black', alpha=0.7)
    ax.add_collection(collection)

ax.autoscale()
ax.axis('equal')
ax.axis('off')
plt.show()
'''
# 测试2

# grid 是 Polygon 或 MultiPolygon
N = 169
grid1 = generate_truncated_ring_L(N)
grid2 = generate_truncated_ring_M4(N)
grid3 = generate_truncated_ring_S(N)
grid4 = generate_truncated_ring_M4_2(N)
grid5 = generate_truncated_ring_M3(N)
grid6 = generate_truncated_ring_M2(N)
grid7 = generate_truncated_ring_M1(N)
grid8 = generate_truncated_ring_MU(N)
def polygon_area(poly):
    if isinstance(poly, Polygon):
        return poly.area
    elif isinstance(poly, MultiPolygon):
        return sum(p.area for p in poly.geoms)
    else:
        raise ValueError("不是 Polygon 或 MultiPolygon 对象")

print(polygon_area(grid1))
print(polygon_area(grid2))
print(polygon_area(grid3))
print(polygon_area(grid4))
print(polygon_area(grid5))
print(polygon_area(grid6))
print(polygon_area(grid7))
print(polygon_area(grid8))

'''
