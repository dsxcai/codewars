import decimal

class Calculator(object):
  def evaluate(self, string):
    postfix = self.to_postfix(string)

    stack = []
    for i in postfix:
      if i == '+':
        o2 = stack.pop()
        o1 = stack.pop()
        stack.append(o1 + o2)
      elif i == '-':
        o2 = stack.pop()
        o1 = stack.pop()
        stack.append(o1 - o2)
      elif i == '*':
        stack.append(stack.pop() * stack.pop())
      elif i == '/':
        o2 = stack.pop()
        o1 = stack.pop()
        stack.append(o1 / o2)
      else:
        stack.append(i)

    return stack[0]

  PRIORITY = {
    '(': 0,
    '+': 1, '-': 1,
    '*': 2, '/': 2,
    '^': 3,
  }

  def to_postfix(self, string):
    output = []
    stack = []

    for i in string.split(' '):
      if self.isOperator(i):
        if len(stack) == 0 or i == '(':
          stack.append(i)
        elif i == ')':
          while stack[-1] != '(':
            output.append(stack.pop())
          stack.pop()
        else:
          while len(stack) > 0 and self.isGreaterEqual(stack[-1], i):
            output.append(stack.pop())
          stack.append(i)
      else:
        output.append(decimal.Decimal(i))

    while len(stack) > 0:
      output.append(stack.pop())

    return output


  def isGreaterEqual(self, op1, op2):
    if self.PRIORITY[op1] >= self.PRIORITY[op2]:
      return True
    return False


  def isOperator(self, c):
    if c in self.PRIORITY or c == ')':
      return True
    return False


import sys

a = Calculator()
print(a.evaluate(sys.argv[1]))
