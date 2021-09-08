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

    def omnidirectional(self, x_input, y_input):
      x, y = -x_input, y_input
      default = 1500

      if y < 0:
        y = -y
        yDelta = -y
        y = Steer._map(y, 0, 32, 1500, 1000)

      else:
        yDelta = y
        y = Steer._map(y, 0, 32, 1500, 2000)

      
      if x < 0:
        x = -x
        xDelta = -x
        x = Steer._map(x, 0, 32, 1500, 2000)

      else:
        xDelta = x
        x = Steer._map(x, 0, 32, 1500, 1000)

      if y_input > 0:
        self.pi.set_servo_pulsewidth(self.Motor1, default)
        self.pi.set_servo_pulsewidth(self.Motor2, y)
        self.pi.set_servo_pulsewidth(self.Motor3, default)
        self.pi.set_servo_pulsewidth(self.Motor4, y)
      else:
        self.pi.set_servo_pulsewidth(self.Motor1, y)
        self.pi.set_servo_pulsewidth(self.Motor2, default)
        self.pi.set_servo_pulsewidth(self.Motor3, y)
        self.pi.set_servo_pulsewidth(self.Motor4, default)


    def eulerRotate(self, x_input, y_input):
      x, y = -x_input, y_input
      default = 1500

      if y < 0:
        y = -y
        y = Steer._map(y, 0, 32, 1500, 1000)

      else:
        y = Steer._map(y, 0, 32, 1500, 2000)

      
      if x < 0:
        x = -x
        x = Steer._map(x, 0, 32, 1500, 2000)

      else:
        x = Steer._map(x, 0, 32, 1500, 1000)

      self.pi.set_servo_pulsewidth(self.ThrottleL, y)
      self.pi.set_servo_pulsewidth(self.ThrottleR, y)

      if x_input < 0:
        x_inverted = Steer._map(x, 1000, 1500, 2000, 1500)
        self.pi.set_servo_pulsewidth(self.Motor2, x_inverted)

      else:
        self.pi.set_servo_pulsewidth(self.Motor4, x)

    def rotate(self, rotation, direction):

      if direction == 'left':
        signal = Steer._map(rotation, 0, 255, 1500, 2000)
        self.pi.set_servo_pulsewidth(self.Motor2, signal)

      else:
        signal = Steer._map(rotation, 0, 255, 1500, 2000)
        self.pi.set_servo_pulsewidth(self.Motor4, signal)
        


    def omnidrive(self, x_input, y_input, x2_input, y2_input):

      tempx = x_input
      tempy = y_input

      tempx_yukselis = x2_input
      tempy_yukselis = y2_input

      xtemp = int(tempx)
      ytemp = int(tempy)

      x_yukselistemp = int(tempx_yukselis)
      y_yukselistemp = int(tempy_yukselis)

      if (xtemp <= 1 and xtemp >= -1): xtemp = 0
      if (ytemp <= 1 and ytemp >= -1): ytemp = 0
      if (x_yukselistemp <= 1 and x_yukselistemp >= -1): x_yukselistemp = 0
      if (y_yukselistemp <= 1 and y_yukselistemp >= -1): y_yukselistemp = 0


      x = Steer._map(xtemp, -32, 32, 1060, 1940)
      y = Steer._map(ytemp, -32, 32, 1060, 1940)

      x_yukselis = Steer._map(x_yukselistemp, -32, 32, 1060, 1940)
      y_yukselis = Steer._map(y_yukselistemp, -32, 32, 1060, 1940)

      sagon_deger = 1500 + (y - 1500) - (x_yukselis - 1500) - (x - 1500)
      solon_deger = 1500 + (y - 1500) + (x_yukselis - 1500) + (x - 1500)

      sagarka_deger = 1500 + (y - 1500) - (x_yukselis - 1500) + (x - 1500)
      solarka_deger = 1500 + (y - 1500) + (x_yukselis - 1500) - (x - 1500)

      if (sagon_deger > 1940): sagon_deger = 1940
      elif (sagon_deger < 1060): sagon_deger = 1060
      if (solon_deger > 1940): solon_deger = 1940
      elif (solon_deger < 1060): solon_deger = 1060
      if (sagarka_deger > 1940): sagarka_deger = 1940
      elif (sagarka_deger < 1060): sagarka_deger = 1060
      if (solarka_deger > 1940): solarka_deger = 1940
      elif (solarka_deger < 1060): solarka_deger = 1060

      self.pi.set_servo_pulsewidth(self.Motor1, sagarka_deger)
      self.pi.set_servo_pulsewidth(self.Motor2, sagon_deger)
      self.pi.set_servo_pulsewidth(self.Motor3, solarka_deger)
      self.pi.set_servo_pulsewidth(self.Motor4, solon_deger)
      self.pi.set_servo_pulsewidth(self.ThrottleL, y_yukselis)
      self.pi.set_servo_pulsewidth(self.ThrottleR, y_yukselis)


    def forward(self, PWM):
      signal = 1500
      signal = Steer._map(PWM, -16, 16, 1000, 2000)

      self.pi.set_servo_pulsewidth(self.Motor2, signal)
      self.pi.set_servo_pulsewidth(self.Motor4, signal)

    def turn(self, PWM):
      signal = 1500
      signal = Steer._map(PWM, -16, 16, 1000, 2000)
      turnPins = [self.Motor2, self.Motor4]
      #print('Motor2: {} - Motor4: {}'.format(signal, signal))

      if signal > 1500:
        for i in turnPins:
          self.pi.set_servo_pulsewidth(turnPins[1], signal)
          #print('Motor2: {} - Motor4: {}'.format(1500, signal))
      if signal < 1500:
        for i in turnPins:
          self.pi.set_servo_pulsewidth(turnPins[0], signal)
          #print('Motor2: {} - Motor4: {}'.format(signal, 1500))
      
    def hold(self):
      default = 1500
      self.pi.set_servo_pulsewidth(self.Motor1, default)
      self.pi.set_servo_pulsewidth(self.Motor2, default)
      self.pi.set_servo_pulsewidth(self.Motor3, default)
      self.pi.set_servo_pulsewidth(self.Motor4, default)
      self.pi.set_servo_pulsewidth(self.ThrottleL, default)
      self.pi.set_servo_pulsewidth(self.ThrottleR, default)

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