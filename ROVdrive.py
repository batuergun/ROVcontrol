import time
import cv2
import RPi.GPIO as GPIO
import pigpio

class Steer:

    def __init__(self):
      self.pwm = []
      GPIO.setmode(GPIO.BCM)
      self.pi = pigpio.pi()
      # Motor1, Motor2, Motor3, Motor4, ThrottleL, ThrottleF
      # self.outputPins = [22, 24, 26, 28, 16, 18]
      self.outputPins = [25, 8, 7, 12, 23, 24]
      self.Motor1, self.Motor2, self.Motor3, self.Motor4, self.ThrottleL, self.ThrottleR = [25, 8, 7, 12, 23, 24]
      
    def driveSetup(self):
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

    def _map(x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def omnidirectional(self, x, y):
      default = 1500


      self.pi.set_servo_pulsewidth(self.Motor1, default)
      self.pi.set_servo_pulsewidth(self.Motor2, default)
      self.pi.set_servo_pulsewidth(self.Motor3, default)
      self.pi.set_servo_pulsewidth(self.Motor4, default)

    #def eulerRotate(self, x, y):

    def forward(self, PWM):
      signal = 1500
      signal = Steer._map(PWM, -16, 16, 1000, 2000)

      self.pi.set_servo_pulsewidth(self.Motor2, signal)
      self.pi.set_servo_pulsewidth(self.Motor4, signal)

    def turn(self, PWM):
      signal = 1500
      signal = Steer._map(PWM, -16, 16, 1000, 2000)
      turnPins = [self.Motor2, self.Motor4]
      print('Motor2: {} - Motor4: {}'.format(signal, signal))

      if signal > 1500:
        for i in turnPins:
          self.pi.set_servo_pulsewidth(turnPins[1], signal)
          print('Motor2: {} - Motor4: {}'.format(1500, signal))
      if signal < 1500:
        for i in turnPins:
          self.pi.set_servo_pulsewidth(turnPins[0], signal)
          print('Motor2: {} - Motor4: {}'.format(signal, 1500))
      

    def stop(self):
      self.pi.set_servo_pulsewidth(self.Motor1, 0)
      self.pi.set_servo_pulsewidth(self.Motor2, 0)
      self.pi.set_servo_pulsewidth(self.Motor3, 0)
      self.pi.set_servo_pulsewidth(self.Motor4, 0)
      self.pi.set_servo_pulsewidth(self.ThrottleL, 0)
      self.pi.set_servo_pulsewidth(self.ThrottleR, 0)

    def shutdown(self):
      self.pi.set_servo_pulsewidth(24, 0)
      self.pi.stop()
      self.pwm.stop()
      GPIO.cleanup()