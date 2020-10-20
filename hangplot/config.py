class Config:
  def __init__(self):
    self.left = "/sys/class/tacho-motor/motor0"
    self.right = "/sys/class/tacho-motor/motor1"
    self.pen = "/sys/class/tacho-motor/motor2"
    self.width = 425

  def getLeftMotor(self): return self.left
  def getRightMotor(self): return self.right
  def getPenMotor(self): return self.pen
  def getAnchorDistance(self): return self.width
