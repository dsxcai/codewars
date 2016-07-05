#!/usr/bin/env python3

import tokenize
import io

class Interpreter:
  def __init__(self):
    self.vars = {}
    self.functions = {}
    self.Types = {
      'identifier': 0,
      'integer': 1,
      'float': 2,
      'assignment': 3,
      'operator': 4,
      'unknown': None,
    }

    self.PRIORITY = {
      '(': 0,
      '+': 1, '-': 1,
      '*': 2, '/': 2,
      '%': 2, '//': 2,
      '^': 3,
    }

  def input(self, expression):
    right = expression.strip()
    left = None
    result = None

    if not right:
      return None

    if '=' in right:
      (left, right) = right.split('=')

    if right:
      result = self.evaluate(self.to_postfix(self.tokenizer(right)))

    if left:
      v, t = self.tokenizer(left)[0]
      if t == self.Types['identifier']:
        self.vars[v] = result

    return result

  def tokenizer(self, string):
    tokens = tokenize.tokenize(io.BytesIO(string.encode()).readline)
    result = []

    for t, v, _, _, _ in tokens:
      if t == tokenize.NUMBER:
        if '.' in v:
          result.append((v, self.Types['float'],))
        else:
          result.append((v, self.Types['integer'],))
      elif t == tokenize.OP:
        if v == '=':
          result.append((v, self.Types['assignment'],))
        else:
          result.append((v, self.Types['operator'],))
      elif t == tokenize.NAME:
        result.append((v, self.Types['identifier'],))
    return result

  def to_postfix(self, infix):
    output = []
    stack = []

    for v, t in infix:
      if t == self.Types['integer'] or t == self.Types['float'] or t == self.Types['identifier']:
        output.append((v, t,))
      elif t == self.Types['operator']:
        if len(stack) == 0 or v == '(':
          stack.append((v, t,))
        elif v == ')':
          while stack[-1][0] != '(':
            output.append(stack.pop())
          stack.pop()
        else:
          while len(stack) > 0 and self.ishigherpriority(stack[-1][0], v):
            output.append(stack.pop())
          stack.append((v, t,))

    while len(stack) > 0:
      output.append(stack.pop())

    return output

  def ishigherpriority(self, op1, op2):
    p1 = self.PRIORITY[op1]
    p2 = self.PRIORITY[op2]

    if p1 < p2 or (p1 == p2 and op1 == '^'):
      return False
  
    return True

  def evaluate(self, token):
    stack = []
    for v, t in token:
      if v == '+':
        o2 = stack.pop()
        o1 = stack.pop()
        stack.append(o1 + o2)
      elif v == '-':
        o2 = stack.pop()
        o1 = stack.pop()
        stack.append(o1 - o2)
      elif v == '*':
        stack.append(stack.pop() * stack.pop())
      elif v == '/':
        o2 = stack.pop()
        o1 = stack.pop()
        stack.append(o1 / o2)
      elif v == '%':
        o2 = stack.pop()
        o1 = stack.pop()
        stack.append(o1 % o2)
      elif v == '//':
        o2 = stack.pop()
        o1 = stack.pop()
        stack.append(o1 // o2)
      elif v == '^':
        o2 = stack.pop()
        o1 = stack.pop()
        stack.append(o1 ** o2)
      else:
        if t == self.Types['integer']:
          stack.append(int(v))
        elif t == self.Types['float']:
          stack.append(float(v))
        elif t == self.Types['identifier']:
          if v not in self.vars:
            print('ERROR: Invalid identifier. No variable with name \'{}\' was found.'.format(v))
            exit(-1)
          else:
            stack.append(self.vars[v])
        else:
          print('ERROR: Unknown symbol type \'{}\' of \'{}\'.'.format(t, v))
          exit(-2)

    if len(stack) > 1:
      print('ERROR: Invalid expression.')
      exit(-3)
    return stack[0]

###########################

import sys

interpreter = Interpreter();

while True:
  print(interpreter.input(sys.stdin.readline().strip()))
