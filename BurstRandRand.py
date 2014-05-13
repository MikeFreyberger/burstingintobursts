# This is a Python framework to compliment "Peek-a-Boo, I Still See You: Why Efficient Traffic Analysis Countermeasures Fail".
# Copyright (C) 2012  Kevin P. Dyer (kpdyer.com)
# See LICENSE for more details.

import random

from Trace import Trace
from Packet import Packet

# This doesn't allow a Burst to have more than bsize packets. 
# But allows all Bursts less than bsize to stay the same size.

class BurstRandRand:
    @staticmethod
    def applyCountermeasure(trace):
        bsize = random.choice(range(2, 10, 1))
        newTrace = Trace(trace.getId())
        rand = random.choice(range(8,256,8))
        count = 0
        curDir = 0
        for packet in trace.getPackets():
             direction = packet.getDirection()
             length = packet.getLength()
             newlength =  min(length + rand, Packet.MTU)        
             time = packet.getTime()
             newPacket = Packet(direction,
                                time,
                                newlength )
             newTrace.addPacket(newPacket)
            
             if (((direction == 0 and curDir == 0) | (direction == 1 and curDir == 1)) and count < bsize):
                 count +=1
                 
             elif (((direction == 0 and curDir == 0) | (direction == 1 and curDir == 1)) and count == bsize):
                 BurstRandRand.makeDummy(newTrace, length, time, curDir)
                 bsize = random.choice(range(2, 10, 1))
                 count = 0
             else:
                 count = 1
                 if(curDir):
                     curDir = 0
                 else:
                     curDir = 1

        return newTrace

    @staticmethod     
    def makeDummy(newTrace, length, time, curDir):
        templength = min(length+random.choice(range(8,256,8)), Packet.MTU )
        dummyPacket = Packet(0, time, templength)
        newTrace.addPacket(dummyPacket)
