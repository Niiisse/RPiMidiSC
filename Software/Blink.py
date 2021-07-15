import time

  # Blink Class
  #
  # Used for blinking hardware elements. String returned will be original string, or
  # empty string. Second argument can be used to invert empty string (for 7 seg displays)
  #
  # Example usage:
  #   blink(byteString, True)
  #
  # By Niisse (2021-07-13)

class Blink:
  def __init__(self, blinkTime):
    self.blinkTime = blinkTime
    self.blank = False
    self.tic = time.time()
    self.toc = 0

  def timer(self):
    # Takes current time, compares it against old time.

    self.toc = time.time()

    if self.toc - self.tic > self.blinkTime * 2:
      self.tic = time.time()
      self.blank = False
    elif self.toc - self.tic > self.blinkTime:
      self.blank = True


  def blink(self, byteString, inverted):
    # Takes input, returns output
    
    self.timer()

    stringLength = len(byteString)

    if self.blank == True:
      outputByteString = "1" * stringLength if inverted else "0" * stringLength
    else:
      outputByteString = byteString

    return outputByteString