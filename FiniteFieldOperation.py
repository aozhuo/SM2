#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
Created on 2018-5-17

@author: aozhuo
"""
class FiniteFieldOperation:
    # 用扩展欧几里得算法求逆元
    def CalculateInverseElement(self, x, p):
        temp_p = p
        s1, s2 = 1, 0
        t1, t2 = 0, 1
        while True:
            q = int(temp_p / x)
            #将s、t向下滑，这里就是交换数的位置
            s1, s2 = s2, s1 - q * s2
            t1, t2 = t2, t1 - q * t2
            temp_p, x = x, temp_p % x
            if x == 1:
                break
        return t2 % p

    # 两个不同的点相加
    def DifferentPointAdd(self, P1, P2, p):
        x1, y1 = P1
        x2, y2 = P2
        # 这里先判断能否整除，能整除就直接算，不能的话在用扩展欧几里得
        if ((y2 - y1) % (x2 - x1)) == 0:
            t = int((y2 - y1) / (x2 - x1)) %p
        else:
            t = (self.CalculateInverseElement(x2 - x1, p) * (y2 - y1)) % p
        x3 = (t ** 2 - x1 - x2) % p
        y3 = (t * (x1 - x3) - y1) % p
        return x3, y3

    # 两个相同的点相加
    def PointDouble(self, P1, a, p):
        x1, y1 = P1
        # 这个除法应该不是普通的除法吧
        if ((3 * (x1 ** 2) + a) % (2 * y1)) == 0:
            t = int((3 * (x1 ** 2) + a) / (2 * y1)) % p
        else:
            t = (self.CalculateInverseElement(2 * y1, p) * (3 * (x1 ** 2) + a)) % p
        x3 = (t ** 2 - 2 * x1) % p
        y3 = (t * (x1 - x3) - y1) % p
        return x3, y3

    # 整合一下上面两个函数，计算任意两个点相加的情况
    def TwoPointAdd(self, P1, P2, a, p):
        if P1 == P2:
            return self.PointDouble(P1, a, p)
        else:
            return self.DifferentPointAdd(P1, P2, p)

    # 计算倍点
    def CalculateEllipticPoint(self, k, P, a, p):
        multiple_P = P
        for i in range(k):
            multiple_P = self.TwoPointAdd(multiple_P, P, a, p)
        return multiple_P


test = FiniteFieldOperation()
P1 = [10,2]
P2 = [9,6]
x, y = test.PointDouble(P1, 1, 19)
print(x, y)