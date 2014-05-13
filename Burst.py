# This is a Python framework to compliment "Peek-a-Boo, I Still See You: Why Efficient Traffic Analysis Countermeasures Fail".
# Copyright (C) 2012  Kevin P. Dyer (kpdyer.com)
# See LICENSE for more details.

import random

from Trace import Trace
from Packet import Packet

class BurstFixedRand:
    @staticmethod
    def applyCountermeasure(trace):
#        print "dir\tlength\ttime"
        bsize = random.choice(range(2, 10, 1))
        newTrace = Trace(trace.getId())
        count = 0
        curDir = 0
        count = 0
        for packet in trace.getPackets():
             direction = packet.getDirection()
             length = packet.getLength()
             newlength = BurstFixedRand.calcLength(length)
             time = packet.getTime()
             # print direction, "\t", length, "\t", time
             newPacket = Packet(direction,
                                time,
                                newlength )
             newTrace.addPacket(newPacket)
            
             if (((direction == 0 and curDir == 0) | (direction == 1 and curDir == 1)) and count < bsize):
                 count +=1
                 
             elif (((direction == 0 and curDir == 0) | (direction == 1 and curDir == 1)) and count == bsize):
                 BurstFixedRand.makeDummy(newTrace, length, time, curDir)
                 count = 0
             else:
                 count = 1
                 if(curDir):
                     curDir = 0
                 else:
                     curDir = 1
                #             for i in range(count, 3):
    #                Burst.makeDummy(newTrace, length, time, curDir)
    #             count = 1
    #         elif (count < 7):
    #             if(curDir):
    #                 curDir = 0
    #             else:
    #                 curDir = 1
    #             for i in range(count, 7):
    #                 Burst.makeDummy(newTrace, length, time, curDir)
    #             count = 1
       #      elif (count < ):
    #             if(curDir):
    #                 curDir = 0
    #             else:
    #                 curDir = 1
    #             for i in range(count, 12):
    #                 Burst.makeDummy(newTrace, length, time, curDir)
    #             count = 1
    #         else:
    #             if(curDir):
    #                 curDir = 0
    #             else:
    #                 curDir = 1
    #             for i in range(count, 25):
    #                 Burst.makeDummy(newTrace, length, time, curDir)
    #             count = 1
                                         

    #         newTrace.addPacket(newPacket)

        return newTrace
      
    @staticmethod
    def calcLength(packetLength):
        # VALID_PACKETS = [638, 1500]
        # retVal = 0
        # for val in VALID_PACKETS:
        #     if packetLength<=val:
        #         retVal = val
        #         break
        rand = random.choice(range(8,256,8))
        length = min(packetLength+rand, Packet.MTU )
        return length

    @staticmethod     
    def makeDummy(newTrace, length, time, curDir):
        # templength = Packet.MTU
        # if Packet.MTU-length>0:
        #     templength = length+random.choice(range(0,Packet.MTU-length,8))
        # dummyPacket = Packet(curDir,
        #                           time,
        #                          templength)
        # newTrace.addPacket(dummyPacket)
              
        templength = min(length+random.choice(range(8,256,8)), Packet.MTU )
        dummyPacket = Packet(0, time, templength)
        newTrace.addPacket(dummyPacket)
