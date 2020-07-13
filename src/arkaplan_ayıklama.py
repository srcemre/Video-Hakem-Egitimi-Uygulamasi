# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:30:30 2020

@author: esara
"""

import cv2

bg_filpath = '..//img//side-view'
bg_extension = '.jpg'


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
        
def extract_background(videoFile):
    vid_cap = cv2.VideoCapture(videoFile)
    if vid_cap.isOpened():
        fps = vid_cap.get(cv2.CAP_PROP_FPS)
        frame_height = vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_width = vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        frame_count = vid_cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print ('FPS', fps)
        print ('Frame Height', frame_height)
        print ('Frame Width', frame_width)
        print ('Frame Count', frame_count)
        
        frame_count = int(frame_count)
        print ("Extracting background")
        _,img = vid_cap.read()
        avg_img = img

        for fr in range(1, frame_count):
            _,img = vid_cap.read()
            fr_fl = float(fr)
            avg_img = (fr_fl*avg_img + img)/(fr_fl+1)
            printProgressBar(fr,frame_count, prefix = 'Progress:', suffix = 'Complete', length = 25)
        
        print ("Saving background")
        vid_cap.release()
        cv2.imwrite(bg_filpath+"_org"+bg_extension, avg_img)
        cv2.imwrite(bg_filpath+"_set"+bg_extension, avg_img)
    else:
        raise IOError("Could not open video")