# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 15:15:29 2019

@author: Sanij
"""
with open("fighterLinks1", "r",  encoding="utf-8") as f:
    lines = f.readlines()
    print(lines)
with open("fighterLinks1", "w",  encoding="utf-8") as f:
    for line in lines:
        if 'c)' not in line:
            f.write(line)