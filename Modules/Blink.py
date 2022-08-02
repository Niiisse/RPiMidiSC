import time
# By Niisse (2021-07-13)

class Blink:
  """Handles blinking output for hardware elements.

  Returned string is original string or empty string (thus causing output to blink),
  depending on timer. Second argument is used to invert result, for use with the
  7 segment displays.
  Example usage: blink(byteString, True)"""

  def __init__(self, blinkTime):
    self.blinkTime = blinkTime
    self.blank = False
    self.tic = time.time()
    self.toc = 0

  def timer(self):
    """Takes current time, compares it against old time."""

    self.toc = time.time()

    if self.toc - self.tic > self.blinkTime * 2:
      self.tic = time.time()
      self.blank = False
    elif self.toc - self.tic > self.blinkTime:
      self.blank = True


  def blink(self, byteString: str, inverted: bool) -> str:
    """Takes input, returns output"""

    self.timer()

    stringLength = len(byteString)

    if self.blank == True:
      outputByteString = "1" * stringLength if inverted else "0" * stringLength
    else:
      outputByteString = byteString

    return outputByteString
