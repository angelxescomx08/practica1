import time
import rrdtool
from getSNMP import consultaSNMP

def actualizarRRD(ip:str, comunidad:str,puerto:int,inicio:str,fin:str):
    horasInicio = int(inicio.strip('\n').split(" ")[1].split(":")[0])
    minutosInicio = int(inicio.strip('\n').split(" ")[1].split(":")[1])

    horasFin= int(fin.strip('\n').split(" ")[1].split(":")[0])
    minutosFin= int(fin.strip('\n').split(" ")[1].split(":")[1])

    horas = horasFin - horasInicio
    minutos = minutosFin - minutosInicio

    tiempo = (horas*60*60) + (minutos*60)

    tiempoInicio = time.time()
    while 1:
        inmulti = consultaSNMP(comunidad, ip,'1.3.6.1.2.1.2.2.1.12.1',puerto)
        ippackets = consultaSNMP(comunidad, ip,'1.3.6.1.2.1.4.9.0',puerto)
        icmpme = consultaSNMP(comunidad, ip,'1.3.6.1.2.1.5.22.0',puerto)
        segout = consultaSNMP(comunidad, ip,'1.3.6.1.2.1.2.2.1.16.1',puerto)
        datagramsin = consultaSNMP(comunidad, ip,'1.3.6.1.2.1.7.2.0',puerto)

        valor = "N:" + str(inmulti) + ':' + str(ippackets) + ":" + str(icmpme) + ":" + str(segout) + ":" + str(datagramsin) 
        print(valor)
        rrdtool.update(ip+'.rrd', valor)
        # rrdtool.dump('practica1.rrd','practica1.xml')
        time.sleep(1)
        tiempoTranscurrido = time.time() - tiempoInicio
        if(tiempoTranscurrido >= tiempo):
            break

    # if ret:
    #    print (rrdtool.error())
    #    time.sleep(300)
