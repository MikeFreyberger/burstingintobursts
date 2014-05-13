# This is a Python framework to compliment "Peek-a-Boo, I Still See You: Why Efficient Traffic Analysis Countermeasures Fail".
# Copyright (C) 2012  Kevin P. Dyer (kpdyer.com)
# See LICENSE for more details.

import random

from Trace import Trace
from Packet import Packet

class BurstPadAllRand:
    @staticmethod
    def applyCountermeasure(trace):
        bsize = random.choice(range(2,10,1))
        newTrace = Trace(trace.getId())
        count = 0
        curDir = 0
        rand = random.choice(range(8,256,8))
        for packet in trace.getPackets():
             direction = packet.getDirection()
             length = packet.getLength()
             newlength = min( packet.getLength()+rand, Packet.MTU )
             time = packet.getTime()
             newPacket = Packet(direction,
                                time,
                                newlength )
            
            
             if  (direction == 1 and curDir == 1 and (count < bsize)):
                 count +=1
                 newTrace.addPacket(newPacket)
             elif (direction == 1 and curDir == 1 and (count ==  bsize)):
                 BurstPadAllRand.sendDummyAck(newTrace, time)
                 newTrace.addPacket(newPacket)
                 bsize = random.choice(range(2,10,1))
                 count = 1
             elif (direction == 0 and curDir == 0):
                 count = 0
                 newTrace.addPacket(newPacket)
             elif (direction == 1 and curDir == 0):
                 curDir = 1
                 count = 1
                 newTrace.addPacket(newPacket)
             elif (direction == 0 and curDir == 1):
                 BurstPadAllRand.makeDummy(newTrace, length, time, bsize, count, rand)
                 newTrace.addPacket(newPacket)
                 curDir = 0
                 count = 0
                 bsize = random.choice(range(2,10,1))

        return newTrace
   
    @staticmethod
    def sendDummyAck(newTrace, time):
        length = 638
        ack = Packet(0, time, length)
        newTrace.addPacket(ack)


    @staticmethod     
    def makeDummy(newTrace, length, time, bsize, count, rand):
        # templength = Packet.MTU
        # if Packet.MTU-length>0:
        #     templength = length+random.choice(range(0,Packet.MTU-length,8))
        # dummyPacket = Packet(curDir,
        #                           time,
        #                          templength)
        for val in range(count, bsize):
             newlength =  Packet.MTU
             dummyPac = Packet(1, time, newlength)
             newTrace.addPacket(dummyPac)
        
