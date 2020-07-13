# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:42:30 2020

@author: esara
"""

import time
import numpy as np
import cv2

import top_view
import distance
import heatmap
import drawoffside
import speed

bg_filpath = '..//img//side-view_org.jpg'
field_mask_path = '..//img//field_mask.jpg'
vid_filepath = '..//vid//video6.mp4'
writeVedioName = '..//vid//offside.avi'

#filters
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
kernelBig = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))

#arrays
ball_position = []
referee_position = []
resized_r = []
    
def set_resized_r(direction, frame_lenx, x_range = 10, y_range = 10):
    """
    Obje bulunduğu pencerede hangi kenera yaklaştıysa o kenera göre, 
    belirlenen miktarda genişletiyor.
    
    direction = 0 -> up
    direction = 1 -> down
    direction = 2 -> left
    direction = 3 -> right
    
    resized_r[x1,x2,y1,y2]
    """
    global resized_r
    global resized_b
    if(direction == 0):
        if(resized_r[0] != 0):
            resized_r[0] -= x_range
            resized_r[1] -= x_range
    if(direction == 1):
        if(resized_r[1] != frame_lenx):
            resized_r[0] += x_range
            resized_r[1] += x_range
    if(direction == 2):
        if(resized_r[2] != 0):
            resized_r[2] -= y_range
            resized_r[3] -= y_range
    if(direction == 3):
        if(resized_r[3] != frame_lenx):
            resized_r[2] += y_range
            resized_r[3] += y_range
            
            
def on_mouse_click_position (event, x, y, flags, param):
    global referee_position
    global frame
    if event == cv2.EVENT_LBUTTONUP:
        if (len(referee_position) == 0):   
            referee_position.append([x,y])
            cv2.circle(frame,(x,y), 10, (0,0,255), -1)
            print("\nReferee_Location: ",[x,y])
            print("Press Space to continue.") 
        else:
            print('\nThe positions was determined. \nPress Space to continue.')
           
            
def on_mouse_click (event, x, y, flags, param):
    global input_ball
    global frame
    if event == cv2.EVENT_LBUTTONUP:
        input_ball = [[x,y], 'b']
        print("ball_position: ",[x,y]) 
        print("referee_position: ",[param[0],param[1]])
    elif event == cv2.EVENT_RBUTTONUP:
         input_ball = [[0,0], 'null']
        
        
def set_object_pos(cap):
    """
        Fare ile hakemin ilk bulunduğu konumu seçme işlemini yapıyor.
    
    """
    global frame
    ret, frame = cap.read()
    print("\nSet the refree location: ") 
    
    while(1):
        if ret:
            cv2.setMouseCallback('Detection_Frame', on_mouse_click_position, 0)
            cv2.imshow('Detection_Frame', frame)
        else:
            print('Ret: False')
    
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
        if key == ord(' '):
            cv2.destroyWindow('Detection_Frame')
            break
    return frame


def init_frames(frame, resize_x = 50, resize_y = 50):
    """
        Objenin bulunduğu ilk konum merkezde olacak şekilde 
        pencereyi kesme işlemi
        
    """
    global resized_r
    global frame_leny
    global frame_lenx
    
    frame_leny = len(frame)
    frame_lenx = len(frame[0])
    
    resized_r = [referee_position[0][1] - resize_x, 
                 referee_position[0][1] + resize_x, 
                 referee_position[0][0] - resize_y, 
                 referee_position[0][0] + resize_y]
    
    
def image_masks(frame, low_color, high_color):
    """
        Uygulanan maskeleme işlemleri
        bu fonksiyonda yapılıyor.
        
    """
    global kernelBig
    global kernel
    
    masked = cv2.inRange(frame, low_color, high_color)
    # opening
    masked = cv2.dilate(masked, kernelBig, iterations=2)
    masked = cv2.erode(masked, kernelBig, iterations=1)
    # closing
    masked = cv2.erode(masked, kernel, iterations=1)
    masked = cv2.dilate(masked, kernel, iterations=1)
     
    masked = cv2.dilate(masked, kernelBig, iterations=2)
    return masked

def win_Settings(n):
    if (n == 0):
        cv2.namedWindow("Main_Frame", flags=cv2.WINDOW_KEEPRATIO) 
        cv2.moveWindow("Main_Frame", 25, 50) 
        cv2.resizeWindow("Main_Frame", 1850, 450)
        cv2.namedWindow("Detection_Frame", flags=cv2.WINDOW_KEEPRATIO) 
        cv2.moveWindow("Detection_Frame", 25, 50) 
        cv2.resizeWindow("Detection_Frame", 1850, 450)
        cv2.namedWindow("Top_View", flags=cv2.WINDOW_KEEPRATIO)
        cv2.moveWindow("Top_View", 490, 535)
        cv2.resizeWindow("Top_View", 690, 400)
    elif (n == 1):
        cv2.namedWindow("Mask_Frame", flags=cv2.WINDOW_KEEPRATIO)
        cv2.moveWindow("Mask_Frame", 25, 535) 
        cv2.resizeWindow("Mask_Frame", 225,400)
        cv2.namedWindow("Cropped_Frame", flags=cv2.WINDOW_KEEPRATIO)
        cv2.moveWindow("Cropped_Frame", 260, 535) 
        cv2.resizeWindow("Cropped_Frame", 225,400)
    elif (n == 2):
        cv2.namedWindow("Heat_Map_Mask", flags=cv2.WINDOW_KEEPRATIO)
        cv2.moveWindow("Heat_Map_Mask", 490, 535)
        cv2.resizeWindow("Heat_Map_Mask", 690,400)
        cv2.namedWindow("Heat_Map_Color", flags=cv2.WINDOW_KEEPRATIO)
        cv2.moveWindow("Heat_Map_Color", 1190, 535)
        cv2.resizeWindow("Heat_Map_Color", 690,400)

def detect_referee(hg_matrix):
    global referee_position
    global input_ball
    global flag
    
    #İlk açılan pencereler
    win_Settings(0)
    
    #Hakem rengi belirlemek için
    low_color = np.array([35, 0, 150])
    high_color = np.array([85, 170, 255])

    #Daha önce oluşturulan saha içi maske
    area_mask = cv2.imread(field_mask_path)
    
    cap = cv2.VideoCapture(vid_filepath)
    #Hakemin ilk konumunu belirlemek ve konum bulmak için pencere boyutları
    resize_x = 40
    resize_y = 30
    frame = set_object_pos(cap)
    frame = init_frames(frame, resize_x, resize_y)

    x=0; y=0; w=0; h=0;
    
    #Top_view'e konum atmak için arraylar
    input_pts = []
    input_referee = [[0,0], 'r']
    input_ball = [[0,0], 'null']
    feet_coord = [0,0]
    
    #Top_View boyutlarında ısı haritası oluşturma
    heatmap.create_heatmap()
    heat_key = True
    mask_key = False
    
    #-Hakemin her iki saniyedeki hızı    
    print('Starting..\n\n')
    print('Click anywhere on Main_Frame to determine the distance.\n L-Mouse: Choose point\n R-Mouse: Remove point')
    second = 2
    rt = speed.RepeatedTimer(second, speed.flag)
    
    #----- Hakemin tespit edilip işaretlendiği kısım ---------
    while True:
        ret, frame = cap.read()
        
        if ret:
            area_masked = cv2.bitwise_and(frame, area_mask)
            cropped_frame_referee = area_masked[resized_r[0]:resized_r[1],resized_r[2]:resized_r[3]]
            
            #Maskeleme işlemleri
            masked = image_masks(cropped_frame_referee, low_color, high_color)
        
            image, contours, hierarchy = cv2.findContours(masked, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if(len(contours) <= 0):
                cv2.rectangle(cropped_frame_referee, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(frame, (x + resized_r[2], y + resized_r[0]), (x + w + resized_r[2], y + h +resized_r[0]), (0, 255, 0), 2)
            else:
                for contour in contours:
                    (x, y, w, h) = cv2.boundingRect(contour)
  
                    if ( (w < 22 or h < 20) or (w > 40 or h > 45) ): continue
                    feet_coord = [float((x+resized_r[2]) + int(25/2.0)), float((y+resized_r[0]) + 25)]
#                    feet_coord = [x + w/2, y + h)]
                    input_referee = [feet_coord, 'r']
                    cv2.rectangle(cropped_frame_referee, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(frame, (x + resized_r[2], y + resized_r[0]), (x + w + resized_r[2], y + h +resized_r[0]), (0, 255, 0), 2)
                    
                    if (x != 0 and y <= 5):   set_resized_r(0, frame_lenx)
                    if (y >= resize_x*2-h-5): set_resized_r(1,frame_lenx)
                    if (x <= 5 and y != 0):   set_resized_r(2,frame_lenx)
                    if (x >= resize_y*2-w-5): set_resized_r(3,frame_lenx)
            
            cv2.setMouseCallback('Main_Frame', on_mouse_click, [x + resized_r[2],y + resized_r[0]])
            input_pts = [input_referee, input_ball]
            top_img, player_top_points = top_view.create_topview(hg_matrix, input_pts)
            heatmap_mask = heatmap.add(player_top_points[0][0])
            
            ref_speed = speed.cal_speed(time.localtime().tm_sec, player_top_points[0][0])
            top_img = drawoffside.drawspeed(top_img, player_top_points, ref_speed)
            
                
            if (player_top_points[1][1][0] == 'b'):
                rb_distance = distance.cal_distance(player_top_points)
                top_img = drawoffside.drawLine(top_img, player_top_points, rb_distance)
                
            
            
            cv2.imshow('Main_Frame',frame)
            cv2.imshow('Top_View',top_img)
            
            #Gereksiz kalabalık m tuşuna basınca gözükmesi ve kapanması için
            if mask_key:
                win_Settings(1)
                cv2.imshow('Mask_Frame',masked)
                cv2.imshow('Cropped_Frame',cropped_frame_referee)
            else:
                cv2.destroyWindow('Mask_Frame')
                cv2.destroyWindow('Cropped_Frame')
            
        else:
            print("ret, false, video bitti")
            win_Settings(2)
            colored_heatmap = heatmap.colorize(heatmap_mask)
            cv2.imshow('Heat_Map_Mask',heatmap_mask)
            cv2.imshow('Heat_Map_Color',colored_heatmap)
            
        #Tuş takımı
        key = cv2.waitKey(15) & 0xFF
        if key == ord('h'):
            if heat_key:
                win_Settings(2)
                colored_heatmap = heatmap.colorize(heatmap_mask)
                cv2.imshow('Heat_Map_Mask',heatmap_mask)
                cv2.imshow('Heat_Map_Color',colored_heatmap)
                heat_key = False
            else:
                heat_key = True
                cv2.destroyWindow('Heat_Map_Mask')
                cv2.destroyWindow('Heat_Map_Color')
                
        if key == ord('m'):
           if mask_key:
               mask_key = False
           else:
               mask_key = True
                
        if key == ord('q'):
            break
        
    rt.stop()
    cap.release()
    cv2.destroyAllWindows()
