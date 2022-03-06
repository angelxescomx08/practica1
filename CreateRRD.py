#!/usr/bin/env python

import rrdtool
def crearRRD(nombre):
    ret = rrdtool.create(nombre+'.rrd',
                     "--start",'N',
                     "--step",'60',
                     "DS:inmulti:COUNTER:600:U:U",
                     "DS:ippackets:COUNTER:600:U:U",
                     "DS:icmpme:COUNTER:600:U:U",
                     "DS:segout:COUNTER:600:U:U",
                     "DS:datagramsin:COUNTER:600:U:U",
                     "RRA:AVERAGE:0.5:1:20",
                     "RRA:AVERAGE:0.5:1:20",
                     "RRA:AVERAGE:0.5:1:20",
                     "RRA:AVERAGE:0.5:1:20",
                     "RRA:AVERAGE:0.5:1:20")
    if ret:
        print(rrdtool.error())