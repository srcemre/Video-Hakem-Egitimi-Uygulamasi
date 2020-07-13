# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 15:38:24 2020

@author: esara
"""

import cv2

colorRed = (0,0,255)
colorYellow = (0,255,255)

def drawLine(img, pt, text):
    x1 = pt[0][0][0]
    y1 = pt[0][0][1]
    x2 = pt[1][0][0]
    y2 = pt[1][0][1]
    cv2.line(img, (x1, y1), (x2, y2), colorRed, thickness=1, lineType=8, shift=0)
    
    center_x = round((x1+x2)/2)
    center_y = round((y1+y2)/2)
    cv2.putText(img,str(round(text))+'m', (center_x, center_y), cv2.FONT_HERSHEY_COMPLEX,.7,colorYellow,1,cv2.LINE_AA)
    return img

def drawspeed(img, pt, text):
    x1 = pt[0][0][0]
    y1 = pt[0][0][1]
    cv2.putText(img,str(text)+'km/h', (x1+10, y1), cv2.FONT_HERSHEY_COMPLEX,.7,colorYellow,1,cv2.LINE_AA)
    return img


