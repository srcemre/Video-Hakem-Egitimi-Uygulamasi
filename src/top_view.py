# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:52:42 2020

@author: esara
"""

import cv2
import numpy as np
import time

start_time = time.time()
field_corners = np.empty([4,2], dtype = "float32")
field_counter = 0
points = []

def area_masking(frame, points):
    mask = np.zeros_like(frame)
    points = np .array(points, np.int32)
    cv2.fillConvexPoly(mask,points,(255,255,255),8,0)
    return mask

def field_click(event, x, y, flags, param):
    global field_counter
    global points
    if (event == cv2.EVENT_LBUTTONUP):
        if (len(points) >=4):
            print ("Press any key to continue")
        else:
            print("Secilen noktalar:",len(points),"\n",points)
            points.append([x,y])
            field_corners[field_counter, :] = [x,y]
            field_counter +=1
            
            
def create_homography():
    global field_counter
    global side_image
    
    filename_sideview = '..//img//side-view_set.jpg'
    filename_fieldmask = '..//img//field_mask.jpg'
    hgcoord_filepath = '..//txt//hgmatrix.txt'
    points_filepath = '..//txt//points.txt'
    
    side_image = cv2.imread(filename_sideview)
    
    print ("Select the four corners from the Background")
    print ("The corners should be selected: Left-Down, Left-Top, Right-Top, Right-Down")
    
    #Pencere ayarları
    cv2.namedWindow("Side-View", flags=cv2.WINDOW_KEEPRATIO) 
    cv2.moveWindow("Side-View", 25, 50) 
    cv2.resizeWindow("Side-View", 1720, 880)

    cv2.setMouseCallback('Side-View', field_click)
    cv2.imshow('Side-View', side_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    area_mask = area_masking(side_image, points)
    cv2.imwrite(filename_fieldmask, area_mask)
    
    side_view_corners = np.copy(field_corners)
	
    top_view_corners = np.array([[44, 393], [44, 30], [598,30], [598, 393]], dtype  = "float32")

    H = cv2.findHomography(side_view_corners, top_view_corners)[0]
    np.savetxt(hgcoord_filepath, H)
    np.savetxt(points_filepath, points)
    return H
        
def get_newPoint(point):
    hgcoord_filepath = '..//txt//hgmatrix.txt'
    hg_matrix = np.loadtxt(hgcoord_filepath)
    x = point[0]
    y = point[1]
    pts = np.matrix(np.zeros(shape=(1,3)))
    pts[0,:] = np.array([x,y,1], dtype = "float32")
    newPoints = np.empty([1,3], dtype = "float32")
    newPoints = hg_matrix*(pts.T)
    x = int(newPoints[0]/float(newPoints[2]))
    y = int(newPoints[1]/float(newPoints[2]))
    point = [x,y]
    return point

def create_topview(hg_matrix, input_pts):
	filename_topview = '..//img//top-view.jpg'
	
	top_image = cv2.imread(filename_topview)

	pts = np.matrix(np.zeros(shape=(len(input_pts),3)))
	c = 0
	for i in input_pts:
		x,y = i[0][0], i[0][1]
		pts[c,:] = np.array([x,y,1], dtype = "float32")
		c+=1
	player_top_points = list()
	newPoints = np.empty([len(input_pts),3], dtype = "float32")
	c = 0
	for i in pts:
		newPoints = hg_matrix*(i.T)
		x = int(newPoints[0]/float(newPoints[2]))
		y = int(newPoints[1]/float(newPoints[2]))
		if(input_pts[c][1][0] == 'r'):
			cv2.circle(top_image,(x,y),10,(0,0,255),-1)
		elif(input_pts[c][1][0] == 'b'):
			cv2.circle(top_image,(x,y),10,(255,0,0),-1)
		else:
			cv2.circle(top_image,(x,y),3,(255,255,255),-1)
		player_top_points.append([[x, y], input_pts[c][1][0]])
		c +=1
	return top_image, player_top_points

    