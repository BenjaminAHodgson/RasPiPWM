#Libraries
import RPi.GPIO as GPIO
import time



#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
BuzzerPin = 13
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(BuzzerPin, GPIO.OUT)


#PWM setup
GPIO.output(BuzzerPin, True)
buzzer = GPIO.PWM(BuzzerPin, 0.25)
buzzer.start(1)
print("PWM setup...")

# This function uses distance to alter the frequency of our buzzer using PWM #
def setfrequency(distmeasure):
    if distmeasure < 500 and distmeasure > 400:
        return 2
    if distmeasure < 400 and distmeasure > 300:
        return 3
    if distmeasure < 300 and distmeasure > 200:
        return 4
    if distmeasure < 200 and distmeasure > 100:
        return 5
    if distmeasure < 100:
        return 6
    if distmeasure > 500:
        return 0.25
    else:
        return 0.25
 

 # This function converts our echo and trigger GPIO inputs to a distance #
def distance():
    print("Measuring distance...")
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    print("Complete")
    return distance


 
if __name__ == '__main__':
    print("Running...")
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            freq = setfrequency(dist)
            buzzer.ChangeFrequency(freq)
            time.sleep(1)
            
                
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        buzzer.stop()



