# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 16:48:05 2025

@author: 25015
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def boltzmann_probabilities(new_energy,current_energy, k_B=8.617333262145e-5):
    '''
    计算从当前能量状态到新能量状态被接受的玻尔兹曼概率。

    Parameters
    ----------
    new_energy : float
        新的能量值 (eV)
    current_energy : float
        当前能量值 (eV)
    T : float
        温度 (K)，默认 361.15 K (~88°C)
    k_B : float
        玻尔兹曼常数，默认 8.617e-5 eV/K
    Returns
    -------
    prob : float
        接受新能量状态的概率 (0~1)
    '''
    
    # 温度设置 (单位: K)
    T = 361.15  # 88摄氏度
    k_B = 8.617333262145e-5  # eV/K，玻尔兹曼常数 
    factor = 1000
    
    delta_E = new_energy - current_energy #
    prob = np.exp(-delta_E/ (factor*k_B * T))
    return prob

