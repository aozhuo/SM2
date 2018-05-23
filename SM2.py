#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
Created on 2018-5-17

@author: aozhuo
学习了编译dll文件，并使用ctypes模块调用写好的SM3哈希算法
ctypes模块中，C++函数返回值为字符串或数组时不回取，要学一下
"""
import random
from ctypes import *
sm3 = cdll.LoadLibrary("SM3DLL.dll")
class DigitalSigniauress:
    def __index__(self, a, b, p, n, x_G, y_G):
        self.a = a
        self.b = b
        self.p = p
        self.n = n
        self.x_G = x_G
        self.y_G = y_G
        # 这两个值还没算
        self.x_A = x_G
        self.y_A = y_G

    #暂时message是一个ACSII码的list（如：[0x61,0x62,0x63]）,后续可以改为字符串输入
    #输出是一个数组（里面有8个元素）
    def Hash(self, message):
        l = len(message)
        for i in range(l):
            message[i] = chr(message[i])
        test = "".join(message).encode()
        hash_value = (c_uint32 * 8)()
        sm3.Hash(test, 4, hash_value)
        return hash_value

    def GenerateZA(self,entlen_A, ID_A):
        # 这个值还没算
        ENTL_A = entlen_A
        message = ENTL_A + ID_A + self.a + self.b + self.x_G +self.y_G + self.x_A + self.y_A
        return self.Hash(message)

    def GenerateMessage(self, ZA, M):
        return ZA + M

    def GenerateE(self, M):
        return self.Hash(M)

    def GenerateRandom(self):
        k = random.randint(0, self.n)
        return k

    def Calculate_r(self, e, x1):
        return (e + x1) % self.n

    def Calculate_s(self, k, r, dA):
        return (1 / (1 + dA)) * (k - r * dA) % self.n

