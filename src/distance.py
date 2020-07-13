# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 02:05:48 2020

@author: esara
"""

from scipy.spatial import distance
import numpy as np

import top_view

#Önceden alınan sahanın köşe noktaları
points_filepath = '..//txt//points.txt'

#Metre cinsinden saha uzunlukları
pitch_Length = 105.0 
pitch_Width  = 68.0

#Metre cinsinden uzunluklar
def cal_distance(player_top_points):

    points = np.loadtxt(points_filepath)
    
    point_w1 = top_view.get_newPoint([points[0][0], points[0][1]])
    point_w2 = top_view.get_newPoint([points[1][0], points[1][1]])
    
    point_referee = player_top_points[0][0]
    point_ball   = player_top_points[1][0]
    
    objects_euclidean = distance.euclidean(point_referee, point_ball)
    pitchPoints_euclidean = distance.euclidean(point_w1, point_w2)
    
    rb_distance = (pitch_Width * objects_euclidean) / pitchPoints_euclidean
#    print('rb_distance: ', round(rb_distance),'m')
    return rb_distance
 
