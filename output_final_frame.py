# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 10:40:52 2025

@author: 25015
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
from shapely.geometry import Polygon, MultiPolygon
import os

def flatten_polygons(polys):
    result = []
    if isinstance(polys, Polygon):
        result.append(polys)
    elif isinstance(polys, MultiPolygon):
        result.extend(list(polys.geoms))
    elif isinstance(polys, list):
        for p in polys:
            if isinstance(p, Polygon):
                result.append(p)
            elif isinstance(p, MultiPolygon):
                result.extend(list(p.geoms))
    return result
def polygons_to_patches(polygons, facecolor, edgecolor='black', alpha=0.7):
    """
    将 Polygon / MultiPolygon / 列表 转换为 PatchCollection
    """
    patches = []

    if polygons is None:
        polygons = []

    # 如果是单个 Polygon
    if isinstance(polygons, Polygon):
        patches.append(MplPolygon(np.array(polygons.exterior.coords), closed=True))
    # 如果是 MultiPolygon
    elif isinstance(polygons, MultiPolygon):
        for p in polygons.geoms:
            patches.append(MplPolygon(np.array(p.exterior.coords), closed=True))
    # 如果是列表
    elif isinstance(polygons, list):
        for p in polygons:
            if isinstance(p, Polygon):
                patches.append(MplPolygon(np.array(p.exterior.coords), closed=True))
            elif isinstance(p, MultiPolygon):
                for sub in p.geoms:
                    patches.append(MplPolygon(np.array(sub.exterior.coords), closed=True))

    return PatchCollection(patches, facecolor=facecolor, edgecolor=edgecolor, alpha=alpha)
    
def plot_frame(sub, chip_frame, energy_value, title, save_path=None):
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_aspect('equal')
    ax.axis('off')

    # 添加基板
    ax.add_collection(polygons_to_patches(sub, facecolor='orange', alpha=0.5))
    # 添加芯片
    ax.add_collection(polygons_to_patches(chip_frame, facecolor='skyblue', alpha=0.8))

    # 自动缩放坐标
    all_polys = sub if isinstance(sub, list) else [sub]
    all_polys += chip_frame if isinstance(chip_frame, list) else [chip_frame]
    minx = min(p.bounds[0] for p in all_polys)
    miny = min(p.bounds[1] for p in all_polys)
    maxx = max(p.bounds[2] for p in all_polys)
    maxy = max(p.bounds[3] for p in all_polys)
    ax.set_xlim(minx-1, maxx+1)
    ax.set_ylim(miny-1, maxy+1)

    ax.set_title(f'After Self-Alignment,Energy={energy_value:.0f}', fontsize=14)
    plt.tight_layout()

    if save_path:
        os.makedirs(save_path, exist_ok=True)
        plt.savefig(os.path.join(save_path, f'{title}.png'), dpi=150)

    plt.show()
    plt.close(fig)

