import sys


PRIORITY = {
  '(': 0,
  '+': 1, '-': 1,
  '*': 2, '/': 2,
  '^': 3,
}


def to_postfix(string):

  output = []
  stack = []

  for i in string.split(' '):
    if i.isdigit():
      output.append(i)

    if isOperator(i):
      if len(stack) == 0 or i == '(':
        stack.append(i)
      elif i == ')':
        while stack[-1] != '(':
          output.append(stack.pop())
        stack.pop()
      else:
        while len(stack) > 0 and isGreaterEqual(stack[-1], i):
          output.append(stack.pop())
        stack.append(i)

  while len(stack) > 0:
    output.append(stack.pop())

  return output


def isGreaterEqual(op1, op2):
  if PRIORITY[op1] >= PRIORITY[op2]:
    return True
  return False


def isOperator(c):
  if c in PRIORITY or c == ')':
    return True
  return False

print(to_postfix(sys.argv[1]))
