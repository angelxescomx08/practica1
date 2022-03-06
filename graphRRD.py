import sys
import rrdtool
import time
tiempo_actual = int(time.time())
#Grafica desde el tiempo actual menos diez minutos
tiempo_inicial = tiempo_actual - 1800

def graficar(ip,inicio,fin):
    ret = rrdtool.graph(ip+"inmulti.png",
                        "--start",str(inicio),
                        "--end",str(fin),
                        "--vertical-label=Paquetes",
                        "--title=Paquetes multicast",
                        "DEF:paquetes={ip}.rrd:inmulti:AVERAGE".format(ip=ip),
                        "LINE3:paquetes#FF0000:Paquetes")
    ret = rrdtool.graph(ip+"ippackets.png",
                        "--start",str(inicio),
                        "--end",str(fin),
                        "--vertical-label=Paquetes",
                        "--title=Paquetes recibidos IPV4",
                        "DEF:paquetes={ip}.rrd:ippackets:AVERAGE".format(ip=ip),
                        "LINE3:paquetes#FF0000:Paquetes")
    ret = rrdtool.graph(ip+"icmpme.png",
                        "--start",str(inicio),
                        "--end",str(fin),
                        "--vertical-label=Mensajes",
                        "--title=Mensajes de respuesta ICMP",
                        "DEF:paquetes={ip}.rrd:icmpme:AVERAGE".format(ip=ip),
                        "LINE3:paquetes#FF0000:Paquetes")
    ret = rrdtool.graph(ip+"segout.png",
                        "--start",str(inicio),
                        "--end",str(fin),
                        "--vertical-label=Segmentos",
                        "--title=Segmentos enviados incluyendo conexiones actuales pero quitando retransmitidos",
                        "DEF:paquetes={ip}.rrd:segout:AVERAGE".format(ip=ip),
                        "LINE3:paquetes#FF0000:Paquetes")
    ret = rrdtool.graph(ip+"datagramsin.png",
                        "--start",str(inicio),
                        "--end",str(fin),
                        "--vertical-label=Datagramas",
                        "--title=Datagramas recibidos que no puedieron ser entregados por cuestiones distintas a la aplicación del puerto destino",
                        "DEF:paquetes={ip}.rrd:datagramsin:AVERAGE".format(ip=ip),
                        "LINE3:paquetes#FF0000:Paquetes")