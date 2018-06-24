#!/usr/bin/env python
import sys

class RC4:

    def __init__( self, key):
        self.key = key
        self.init()

    def init(self):
        self.S = self.KSA()
        self._keystream = self.PRGA(self.S)


    def KSA(self):
        key = self.key
        keylength = len(key)

        S = range(256)

        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % keylength]) % 256
            S[i], S[j] = S[j], S[i]  # swap

        return S


    def PRGA(self,S):
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]  # swap

            K = S[(S[i] + S[j]) % 256]
            yield K

    def keystream(self):
        self.init()
        return self._keystream

    def getKeystream(self,n):
        self.init()
        res=""
        for i in range(0,n):
            res += format(self._keystream.next(), '#04x')[2:]
        return res
            
        

            



   



    


