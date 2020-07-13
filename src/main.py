# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:27:04 2020

@author: esara
"""

import os
import numpy as np

import hakem_tespiti
import arkaplan_ayıklama
import top_view

#os.chdir('C:\\Users\\esara\\Desktop\\videohakem\\src')

vid_filepath = '..//vid//video6.mp4'
background_filepath = '..//img//side-view_org.jpg'
hgmatrix_filepath = '..//txt//hgmatrix.txt'

def main():
    if(not os.path.isfile(background_filepath)):
        if(not os.path.exists('..//img')):
            os.mkdir('..//img')
        print ("Background has not been extracted, will extract.")
        arkaplan_ayıklama.extract_background(vid_filepath)
    print ("Background image found")
    
    if(not os.path.isfile(hgmatrix_filepath)):
        if(not os.path.exists('..//txt')):
            os.mkdir('..//txt')
        print ("Homography matrix has not been created.")
        top_view.create_homography()
    hg_matrix = np.loadtxt(hgmatrix_filepath)
    print ("Homography matrix found")
    print (hg_matrix)
	
    hakem_tespiti.detect_referee(hg_matrix)
	
main()
