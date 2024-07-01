import math


def absolute_value(arg1):
    return round(abs(arg1), 2)

def add(arg1, arg2):
    return round(arg1 + arg2, 2)

def acos(arg1):
    return round(math.acos(arg1), 2)

def asin(arg1):
    return round(math.asin(arg1), 2)

def atan(arg1):
    return round(math.atan(arg1), 2)

def cos(arg1):
    return round(math.cos(arg1), 2)

def cosh(arg1):
    return round(math.cosh(arg1), 2)

def divide(arg1, arg2):
    return round(arg1 / arg2, 2)

def factorial(arg1):
    return round(math.factorial(arg1), 2)

def log(arg1):
    return round(math.log(arg1), 2)

def multiply(arg1, arg2):
    return round(arg1 * arg2, 2)

def power(arg1, arg2):
    return round(arg1 ** arg2, 2)

def square_root(arg1):
    return round(math.sqrt(arg1), 2)

def subtract(arg1, arg2):
    return round(arg1 - arg2, 2)

def sin(arg1):
    return round(math.sin(arg1), 2)

def sinh(arg1):
    return round(math.sinh(arg1), 2)

def tan(arg1):
    return round(math.tan(arg1), 2)

def tanh(arg1):
    return round(math.tanh(arg1), 2)

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False