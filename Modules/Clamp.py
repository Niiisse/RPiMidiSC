# Simple clamp
# Example usage:
#
#   clamp(value, min, max)
# 
# by Niisse on 2021-07-20

def clamp(self, value, min, max):
  if value > max:
    return min

  elif value < min:
    return min

  else:
    return value