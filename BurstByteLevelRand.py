# This is a Python framework to compliment "Peek-a-Boo, I Still See You: Why Efficient Traffic Analysis Countermeasures Fail".
# Copyright (C) 2012  Kevin P. Dyer (kpdyer.com)
# See LICENSE for more details.

import random

from Trace import Trace
from Packet import Packet

class BurstByteLevelRand:
    @staticmethod
    def applyCountermeasure(trace):
        bsize = random.choice(range(3000, 15000, 8))
        rand = random.choice(range(8,256,8))
        newTrace = Trace(trace.getId())
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
            
            
             if  (direction == 1 and curDir == 1 and (count+newlength < bsize)):
                 count +=newlength
                 newTrace.addPacket(newPacket)
             elif (direction == 1 and curDir == 1 and (count+newlength >= bsize)):
                 pad = bsize - count
                 packetFirstHalf = Packet(1, time, pad)
                 newTrace.addPacket(packetFirstHalf)
                 BurstByteLevelRand.sendDummyAck(newTrace, time)
                 count = newlength-pad
                 finishPacket = Packet(1, time, count)
                 newTrace.addPacket(finishPacket)
                 bsize = random.choice(range(3000, 15000, 8))
             elif (direction == 0 and curDir == 0):
                 count = 0
                 newTrace.addPacket(newPacket)
             elif (direction == 1 and curDir == 0):
                 curDir = 1
                 count = newlength
                 newTrace.addPacket(newPacket)
             elif (direction == 0 and curDir == 1):
                 BurstByteLevelRand.makeDummy(newTrace, length, time, bsize, count, rand)
                 newTrace.addPacket(newPacket)
                 curDir = 0
                 count = 0
                 bsize = random.choice(range(3000, 15000, 8))
                         
        return newTrace
      
    @staticmethod
    def sendDummyAck(newTrace, time):
        length = 638
        ack = Packet(0, time, length)
        newTrace.addPacket(ack)


    @staticmethod     
    def makeDummy(newTrace, length, time, bsize, count, rand):
        bytestoadd = bsize - count - length
        leftover = length - (bsize-count)
        if (bytestoadd < 0):
            padpacket = Packet(1, time, bsize-count)
            newTrace.addPacket(padpacket)
            BurstByteLevelRand.sendDummyAck(newTrace, time)
            finishdata = Packet(1, time, leftover+rand)
            newTrace.addPacket(finishdata)
            count = leftover+rand
        else:
            neededdata = Packet(1, time, length)
            newTrace.addPacket(neededdata)
            while(bytestoadd > 1500):
                length = random.choice(range(256, 1500, 8))
                bytestoadd -= length
                temppac = Packet(1, time, length)
                newTrace.addPacket(temppac)
            lastpac = Packet(1, time, bytestoadd)
            newTrace.addPacket(lastpac)
        
