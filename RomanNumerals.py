import collections

class RomanNumerals(object):
  Rm = collections.OrderedDict([('I', 1) , ('V', 5), ('X', 10), ('L', 50), ('C', 100), ('D', 500), ('M', 1000)])
  R = Rm.keys()

  def from_roman(self, number):
    stack = []
    for i in number:
      if len(stack) > 0 and self.Rm[i] > stack[-1]:
        stack.append(self.Rm[i] - stack.pop())
      else:
        stack.append(self.Rm[i])

    return sum(stack)

  def to_roman(self, number):
    N = [int(i) for i in '{:04d}'.format(number)]
    s = ''
    idx = 6

    for n in N:
      if n <= 3:
        s += self.R[idx] * n
      elif n == 4:
        s += self.R[idx] + self.R[idx + 1]
      elif n == 5:
        s += self.R[idx + 1]
      elif n <= 8:
        s += self.R[idx + 1] + self.R[idx] * (n - 5)
      elif n == 9:
        s += self.R[idx] + self.R[idx + 2]
      else:
        print('err')
      idx = idx - 2

    return s