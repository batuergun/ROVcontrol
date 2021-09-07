import time
import cv2
import RPi.GPIO as GPIO
import pigpio

class Steer:

    def __init__(self):
      self.pwm = []

      # Motor1, Motor2, Motor3, Motor4, ThrottleL, ThrottleF
      # self.outputPins = [22, 24, 26, 28, 16, 18]
      self.outputPins = [25, 8, 7, 12, 23, 24]
      self.Motor1, self.Motor2, self.Motor3, self.Motor4, self.ThrottleL, self.ThrottleF = [25, 8, 7, 12, 23, 24]
      
    def driveSetup(self):
      GPIO.setmode(GPIO.BCM)
      self.pi = pigpio.pi()
      for i in self.outputPins:
        self.pi.set_servo_pulsewidth(i, 1500)
        time.sleep(2)

        self.pi.set_servo_pulsewidth(i, 1000)
        time.sleep(2)

        self.pi.set_servo_pulsewidth(i, 1200)
        time.sleep(2)

        self.pi.set_servo_pulsewidth(i, 1500)
        time.sleep(2)

    def targetEvaluation(targetList):
        print(targetList)

    def forward(self, PWM):
      #forwardPins = [self.Motor2, self.Motor4]
      #for i in forwardPins:
        self.pi.set_servo_pulsewidth(self.Motor2, PWM)
        self.pi.set_servo_pulsewidth(self.Motor4, PWM)

    def turn(self, PWM, acceleration, angle):
      turnPins = [self.Motor2, self.Motor4]
      if angle > 0:
        for i in turnPins:
          self.pi.set_servo_pulsewidth(turnPins[i], PWM)
      if angle < 0:
        for i in turnPins:
          self.pi.set_servo_pulsewidth(turnPins[i], PWM)

    def shutdown(self):
      self.pi.set_servo_pulsewidth(24, 0)
      self.pi.stop()
      self.pwm.stop()
      GPIO.cleanup()