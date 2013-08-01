#!/usr/bin/env python
#*-*coding:utf-8*-*

import threading
import time

__author__ = 'Tony Liu'

class TimerUtil:

    def __init__(self):
        self.counter = 1

    '''添加一次性的回调任务
    user_callback 回调
    second 多少秒
    return uniqueId
    '''
    def start_once_timer(self, seconds, user_callback = None, *args, **kargs):
        timer_name = "timer." + str(self.counter) 
        self.counter += 1
        timer = VeCoreTimer(interval = seconds, user_callback = user_callback, \
            is_reply = False, timer_name = timer_name, *args, **kargs)
        timer.start()

        return timer


    '''添加重复的回调任务    
    second 多少秒
    user_callback 回调
    return timer
    '''
    def start_repeat_timer(self, seconds, user_callback, *args, **kargs):
        timer_name = "timer." + str(self.counter) 
        self.counter += 1
        timer = VeCoreTimer(interval = seconds, user_callback = user_callback, \
            is_reply = True, timer_name = timer_name, *args, **kargs)
        timer.start()

        return timer

    '''删除一次性或者重复的回调任务
    timer timer instance
    '''
    def stop_timer(self, timer):        
        timer.stop()


class VeCoreTimer(threading.Thread):
    def __init__(self, interval, user_callback = None, is_reply = False, \
        timer_name = None, *args, **kargs):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.interval = interval
        self.user_args = (user_callback, args, kargs)
        self.is_reply = is_reply    
        self.timer_name = timer_name or "timer_" + str(int(time.time()))
        self.is_force_stop = False        

    def run(self):        
        if self.is_reply == False:
            while not self.event.is_set() and self.interval > 0:                
                self.interval -= 1
                self.event.wait(1)

            if self.is_force_stop == False:
                func, args, kargs = self.user_args 
                func(*args, **kargs)
        else:
            timeout = self.interval
            while not self.event.is_set():
                timeout -= 1                
                if timeout <= 0:
                    func, args, kargs = self.user_args 
                    func(*args, **kargs)
                    timeout = self.interval
                self.event.wait(1)

    def stop(self):
        self.is_force_stop = True
        self.event.set()


if __name__ == '__main__':
    def test1(val1):
        print("hi,wrold1,", val1)    

    def test2(val):
        print("hi,wrold2,", val)  

    def test3(val, timer):
        print("hi,wrold3,", val)   
        timerUtil.stop_timer(timer)

    timerUtil = TimerUtil()
    timer1 = timerUtil.start_once_timer(3, test1, val1="timer1")
    timer2 = timerUtil.start_once_timer(10, test2, val="timer2")
    timer3 = timerUtil.start_once_timer(2, test3, val="timer3", timer=timer2)
    timer4 = timerUtil.start_repeat_timer(1, test1, val1="timer4")
    time.sleep(20)
    timerUtil.stop_timer(timer4)
