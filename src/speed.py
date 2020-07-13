# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 15:38:24 2020

@author: esara

RepeatedTimer classı sayesinde, cal_speed fonksiyonunu belirlenen saniye aralıklarıyla çağırıyoruz.
Örneğin 2 saniyede bir çağırsın. İlk çağırmada çağırdığı zamanı ve hakemin pozisyonunu kaydediyor.
2 saniye sonra tekrar çağırdığında geçen zamanı bulup, hakemin aldığı kuş bakışı mesafeyi bulup 
yaklaşık hızını hesaplıyor.

"""
from threading import Timer
import distance
import cv2

prevTime = 0
prevPoints = [[0,0]]
speed = 0
flag1 = True
flag2 = False

def cal_speed(time, points):
    global prevTime
    global prevPoints
    global speed
    global flag1, flag2
    
    if flag2:
        #ilk defa çalışacaksa flag1 e giriyor
        if flag1:
            prevTime = time
            prevPoints = points
            flag1 = False
            flag2 = False
            return round(speed,1)
        else:
            input_points = [prevPoints,points]
            ds = distance.cal_distance(input_points)
            sec = abs(time - prevTime)
            speed = round((ds/sec),2) # m/s
            speed = speed * (60*60)/1000
#            print('ds:',ds,' sec:',sec,' Speed:', round(speed,1),'km/h')
            flag2 = False
            prevTime = time
            prevPoints = points
            return round(speed,1)
    else:
        return round(speed,1)

def flag():
    global flag2
    flag2 = True
        
#Her belirlenen saniye fonksiyonu çağırmak için oluşturulmuş class
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
        

