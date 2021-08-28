import cv2

class Steer:

    def __init__(self, target):
        
        self.target = target

    def targetEvaluation(self, targetList):
        print(targetList)