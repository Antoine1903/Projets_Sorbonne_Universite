from prime import is_probable_prime
from math import sqrt
import random


#Exercice 1
#Q1
def bezout(a, b):
    if b==0: 
        return a, 1, 0
    pgcd, u1, v1 = bezout(b, a % b)
    u = v1
    v = u1 - (a // b) * v1
    return pgcd, u, v

#Q2
def inv_mod(a, n):
    _, u, _ = bezout(a, n)
    return u % n


def invertibles(N):
    return


#Q3
def phi(N):
    return


#Exercice 2
#Q1
def exp(a, n, p):
    return


#Q2
def factor(n):
    return


#Q3
def order(a, p, factors_p_minus1):
    return


#Q4
def find_generator(p, factors_p_minus1):
    return


#Q5
def generate_safe_prime(k):
    return


#Q6
def bsgs(n, g, p):
    return
