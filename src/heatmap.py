# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 16:36:03 2020

@author: esara
"""
import numpy as np
import cv2

filename_topview = '..//img//top-view.jpg'
heatmap_mask = []

#Ayarlar
circle_size = 12
opacity = 0.005

def create_heatmap():
    global heatmap_mask
    top_image = cv2.imread(filename_topview)
    heatmap_mask = np.zeros([len(top_image[:,0]),len(top_image[0,:])])
    return heatmap_mask

def add(cords):
    overlay = heatmap_mask.copy()
    cv2.circle(overlay, (cords[0], cords[1]), circle_size, 1, -1)
    cv2.addWeighted(overlay, opacity, heatmap_mask, 1 - opacity, 0, heatmap_mask)
    return heatmap_mask

def colorize(heatmap_mask):
    
    heatmap_top_image = cv2.imread(filename_topview)
    
    X = len(heatmap_mask[0,:])
    Y = len(heatmap_mask[:,0])
   
    kernel = np.ones((10,10),np.float32)/50
    heatmap_mask = cv2.filter2D(heatmap_mask,-1,kernel)
    
    for x in range(0,X):
        for y in range(0,Y):

            if(heatmap_mask[y,x] <= 0.2 and heatmap_mask[y,x] >= 0.1 ):
                heatmap_top_image[y,x,0] = 0
                heatmap_top_image[y,x,1] = 255
                heatmap_top_image[y,x,2] = 0
            elif(heatmap_mask[y,x] <= 0.4 and heatmap_mask[y,x] >= 0.2 ):
                heatmap_top_image[y,x,0] = 0
                heatmap_top_image[y,x,1] = 255
                heatmap_top_image[y,x,2] = 127
            elif(heatmap_mask[y,x] <= 0.6 and heatmap_mask[y,x] >= 0.4 ):
                heatmap_top_image[y,x,0] = 0
                heatmap_top_image[y,x,1] = 255
                heatmap_top_image[y,x,2] = 255
            elif(heatmap_mask[y,x] <= 0.8 and heatmap_mask[y,x] >= 0.6 ):
                heatmap_top_image[y,x,0] = 0
                heatmap_top_image[y,x,1] = 127
                heatmap_top_image[y,x,2] = 255
            elif(heatmap_mask[y,x] >= 0.8):
                heatmap_top_image[y,x,0] = 0
                heatmap_top_image[y,x,1] = 0
                heatmap_top_image[y,x,2] = 255

    return heatmap_top_image

#%% TEST

def test():
    img = create_heatmap()
    heat_key = True
    for i in range(0,500):
        img = add((i,i))
    img = colorize(heat_key, img)
    cv2.imshow('s',img)    

#test()