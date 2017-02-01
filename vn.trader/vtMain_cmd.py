# encoding: UTF-8
import sys
import ctypes
import datetime

from mail import *
from vtEngine import MainEngine
from eventEngine import *
from riskManager.rmEngine import RmEngine
#----------------------------------------------------------------------
class EventLoopManager(object):
    def __init__(self):
        self.makeLog('Event loop manager started', False)
        self.engineStarted = False
        self.mainEngine = MainEngine()
        self.eventEngine = EventEngine2()
        print "connect MongoDB.........."
        self.mainEngine.dbConnect()
        time.sleep(5)
    
        print "connet CTP.........."
        self.mainEngine.connect('CTP')
        time.sleep(5)
    
        print "start strategy double ema......."
        self.mainEngine.ctaEngine.loadSetting()
        self.mainEngine.ctaEngine.initStrategy('double ema')
        
    def start(self):
        self.eventEngine.start()
        # 注册事件监听
        self.registerEvent()
        
    def onEventLog(self, event):
        log = event.dict_['data']
        logContent = ''.join([log.logTime, log.logContent, '\n'])
        self.makeLog(logContent)
        
    def onEventTimer(self, event):
        today = date.weekday(datetime.now().date())
        if today == 5 or today == 6:#weekends
            return
        hour =  datetime.now().hour
        
        #log in
        if(self.engineStarted == False 
           and (hour in [9, 10, 11, 13, 20, 21, 22, 23, 24, 1])#trading hour
           ):
            self.engineStarted = True
            self.makeLog('Starting CTP double ema')
            self.run()
            return
        
        #log out
        if(self.engineStarted == True 
           and (hour in [14, 2])
           ):
            self.makeLog('Ending CTP double ema')
            self.stop()
            self.engineStarted = False
            return        
        
    def registerEvent(self):
        """注册事件监听"""
        self.mainEngine.eventEngine.register(EVENT_LOG, self.onEventLog)
        self.mainEngine.eventEngine.register(EVENT_CTA_LOG, self.onEventLog)
        self.eventEngine.register(EVENT_TIMER, self.onEventTimer)
        self.makeLog('Events registerred',False)
        
    def run(self):
        self.mainEngine.ctaEngine.startStrategy('double ema')
        self.engineStarted = True
        
    def stop(self):
        try:
            self.mainEngine.ctaEngine.stopStrategy('double ema')
            #self.mainEngine.exit()
            self.engineStarted = False
        except Exception as e:
            print e
        
    def makeLog(self, content, sendemail = False):
        if sendemail == True:
            send_email(subject = content)
        print content
        
if __name__ == '__main__':
    import time
    manager = EventLoopManager()
    manager.start()
