# This is a Python framework to compliment "Peek-a-Boo, I Still See You: Why Efficient Traffic Analysis Countermeasures Fail".
# Copyright (C) 2012  Kevin P. Dyer (kpdyer.com)
# See LICENSE for more details.

import random

from Trace import Trace
from Packet import Packet

# This doesn't allow a Burst to have more than bsize packets. 
# But allows all Bursts less than bsize to stay the same size.

class BurstClient2Server:
    @staticmethod
    def applyCountermeasure(trace):
        bsize = random.choice(range(3, 4, 1))
        dsize = random.choice(range(3, 4, 1))
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
            
             if ((direction == 1 and curDir == 1) and count < bsize):
                 count +=1
                 newTrace.addPacket(newPacket)
             elif ((direction == 1 and curDir == 1) and count == bsize):
                 BurstClient2Server.makeDummy(newTrace, length, time, curDir, dsize)
                 newTrace.addPacket(newPacket)
                 count = 1
             elif ((direction == 1 and curDir == 0)):
                 newTrace.addPacket(newPacket)
                 curDir = 1
                 count = 1
             elif ((direction == 0 and curDir == 1)):
                 newTrace.addPacket(newPacket)
                 curDir = 0
                 count = 1
             elif (direction == 0 and curDir == 0):
                 newTrace.addPacket(newPacket)
                 count = 1
        return newTrace

    @staticmethod     
    def makeDummy(newTrace, length, time, curDir, dsize):
#        templength = min(length+random.choice(range(8,256,8)), Packet.MTU )
       # dummyPacket = Packet(0, time, 638)
      #  newTrace.addPacket(dummyPacket)
        for val in range(0, dsize):
            newlength = random.choice(range(638,912,8))
#           newlength = 638
            dummyPacket = Packet(0, time, newlength)
            newTrace.addPacket(dummyPacket)
