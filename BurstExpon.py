# This is a Python framework to compliment "Peek-a-Boo, I Still See You: Why Efficient Traffic Analysis Countermeasures Fail".
# Copyright (C) 2012  Kevin P. Dyer (kpdyer.com)
# See LICENSE for more details.

import random

from Trace import Trace
from Packet import Packet

class BurstExpon:
    @staticmethod
    def applyCountermeasure(trace):
        newTrace = Trace(trace.getId())
        count = 0
        curDir = 0
        rand = random.choice(range(8,256,8))
        count = 0
        for packet in trace.getPackets():
             direction = packet.getDirection()
             length = packet.getLength()
             newlength =  min(length + rand, Packet.MTU) 
             time = packet.getTime()
             newPacket = Packet(direction,
                                time,
                                newlength )
            
            
             if  ((direction == 1 and curDir == 1)):
                 count +=1
                 newTrace.addPacket(newPacket)
             elif (direction == 0 and curDir == 0):
                 count = 0
                 newTrace.addPacket(newPacket)
             elif (direction == 1 and curDir == 0):
                 curDir = 1
                 count = 1
                 newTrace.addPacket(newPacket)
             elif (direction == 0 and curDir == 1):
                 BurstExpon.makeDummy(newTrace, length, time, curDir, count, rand)
                 newTrace.addPacket(newPacket)
                 curDir = 0
                 count = 0

        return newTrace
        
    @staticmethod     
    def makeDummy(newTrace, length, time, curDir, count, rand):
        VALID_PACKETS = [4,8,16,32,64]
        retVal = 0
        for val in VALID_PACKETS:
            if count<=val:
                retVal = val
                break
        for val in range(count, retVal):
            templength = min(length+rand, Packet.MTU )
            dummyPacket = Packet(1, time, templength)
            newTrace.addPacket(dummyPacket)
