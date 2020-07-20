import time
from datetime import datetime
from config import alarms, duration 
import RPi.GPIO as GPIO

def nextAlarm(alarms):
    curTime = datetime.now().strftime("%H:%M:%S")
    nextAlarm = ""
    for alarm in alarms:
        hour = False
        minute = False
        second = False
        if (int(alarm[0:2]) >= int(curTime[0:2])):
            hour = True
        if (int(alarm[3:5]) >= int(curTime[3:5])):
            minute = True    
        if (int(alarm[6:8]) >= int(curTime[6:8])):
            second = True
        if minute and not hour:
            continue
        elif alarm[0:2] == curTime[0:2] and not minute:
            continue
        elif hour:
            return alarm
        
    return alarms[0]
        
            
        #elif not hour and minute:
        #    return alarms[0]



try:
    buzzerPin = 21
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzerPin, GPIO.OUT)
    GPIO.output(buzzerPin, GPIO.LOW)

    curTime = datetime.now().strftime("%H:%M:%S")
    print("Break Timer Activated\nCurrent Time: " + curTime)
    print("Next Alarm At: " + str(nextAlarm(alarms)))
    while(True):
        curTime = datetime.now().strftime("%H:%M:%S")
        curAlarm = alarms.pop(0)
        
        if(curTime == curAlarm):
            start = time.time()
            print("Buzz Start: " + curTime)
            GPIO.output(buzzerPin, GPIO.HIGH)
            while (time.time() - start < duration):
                pass
            GPIO.output(buzzerPin, GPIO.LOW)
            print("Buzz end: " + str(time.time()- start))
            print("Next Alarm At: " + str(nextAlarm(alarms)))
        alarms.append(curAlarm)
        
    GPIO.cleanup()
except KeyboardInterrupt:
    print("Program Terminated")
    GPIO.cleanup()
    

    
