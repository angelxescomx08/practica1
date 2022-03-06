import os
import time
import sys

from getSNMP import consultaSNMP
from SNMP import consultaSNMPInterfaces
from CreateRRD import crearRRD
from graphRRD import graficar
from updateRRD import actualizarRRD
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

#colores para la consola
amarillo = "\x1b[1;33m"

def borrarPantalla():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system("cls")

#retornar las lineas del archivo
def leerArchivo() -> list:
    archivo = open('dispositivos.txt', 'r')
    lineas = archivo.readlines()
    archivo.close()
    return lineas

def escribirArchivo(linea:str,modo="a"):
    archivo = open('dispositivos.txt',modo)
    archivo.writelines("\n"+linea)
    archivo.close()

def escribirAgenteArchivo(linea:str,modo="a"):
    archivo = open('dispositivos.txt',modo)
    archivo.write(linea)
    archivo.close()

def agregarDispositivo():
    print('{color}Ingresa la dirección IP del dispositivo a agregar'.format(color=amarillo))
    ip = input().strip('\n')
    print('{color}Ingresa la versión SNMP (v1,v2,v3)'.format(color=amarillo))
    version = input().strip('\n')
    print('{color}Ingresa la comunidad'.format(color=amarillo))
    comunidad = input().strip('\n')
    print('{color}Ingresa el puerto'.format(color=amarillo))
    puerto = input().strip('\n')
    escribirAgenteArchivo('{ip} {version} {comunidad} {puerto}'
        .format(ip=ip,version=version,comunidad=comunidad,puerto=puerto))
    

def eliminarDispositivo():
    print('{color}Ingresa la dirección IP del dispositivo a eliminar'.format(color=amarillo))
    dispositivo = input()
    lineas = leerArchivo()
    archivo = open('dispositivos.txt','w')
    archivo.truncate()
    archivo.close()
    for i in range(len(lineas)):
        if dispositivo.strip('\n') in lineas[i]:
            pass
        else:
            if(i==len(lineas)-1):
                escribirAgenteArchivo(lineas[i],"w")
            else:
                escribirAgenteArchivo(lineas[i],"w")

def imprimirDatosDispositivos():
    borrarPantalla()
    print('{color}Número de agentes en monitoreo {num}'.format(color=amarillo,num=len(leerArchivo())))
    lineas = leerArchivo()
    for linea in lineas:
        datos = linea.strip('\n').split(" ")
        ip = datos[0]
        comunidad = datos[2]
        puerto = int(datos[3])
        numInterfaces = int(consultaSNMP(comunidad,ip,'1.3.6.1.2.1.2.1.0',puerto))
        
        conectividadCodigo = int(consultaSNMP(comunidad,ip,'1.3.6.1.2.1.2.2.1.8.2',puerto))
        print("CONECTIVIDAD:",conectividadCodigo)
        conectividad = ""
        if(conectividadCodigo==1):
            conectividad= "UP"
        else:
            conectividad= "DOWN"

        print('{color}Conectividad: {conectividad}, Número de interfaces de red {ip}: {num}'
            .format(color=amarillo,conectividad=conectividad,ip=ip,num=numInterfaces))
        
        #interfaces de de red informacion
        for num in range(1,numInterfaces+1):
            estatus = int(consultaSNMP(comunidad,ip,'1.3.6.1.2.1.2.2.1.8.'+str(num),puerto))
            print("\t"+str(num)+".")
            if(estatus==1):
                print("\t\tEstatus: UP")
            elif estatus==2:
                print("\t\tEstatus: DOWN")
            else:
                print("\t\tEstatus: TESTING")
            adminEstatus = int(consultaSNMP(comunidad,ip,'1.3.6.1.2.1.2.2.1.7.'+str(num),puerto))
            if(adminEstatus==1):
                print("\t\tAdmin estatus: UP")
            elif adminEstatus==2:
                print("\t\tAdmin estatus: DOWN")
            else:
                print("\t\tAdmin estatus: TESTING")
            descripcion = str(consultaSNMPInterfaces(comunidad,ip,'1.3.6.1.2.1.2.2.1.2.'+str(num)))
            if('0x' in descripcion):
                descripcion = bytes.fromhex(descripcion[3:]).decode('ASCII')
            
            print("\t\t"+'Descripción:'+descripcion)

def generarPDF(comunidad,ip,puerto):
    res = consultaSNMP(comunidad,ip,"1.3.6.1.2.1.1.1.0",puerto)
    if(len(res.split("Software")) > 1):
        sistema = res.split("Software")[1].split(" ")[1]
        version = res.split("Software")[1].split(" ")[3]
    else:
        sistema = res.split(" ")[1]
        version = res.split(" ")[3]
    ubicacion = consultaSNMP(comunidad,ip,"1.3.6.1.2.1.1.6.0",puerto)
    tiempo = consultaSNMP(comunidad,ip,"1.3.6.1.2.1.1.3.0",puerto)
    tiempo ="{0:.2f}".format(((int(tiempo)*0.01)/60)/60)

    c = canvas.Canvas(ip+".pdf",pagesize=A4)
    w, h = A4

    if(sistema == "Linux"):
        c.drawImage("linux.png",10,h-60,width=50,height=50)
    else:
        c.drawImage("windows.png",10,h-60,width=50,height=50)
    c.setFont("Helvetica", 10)
    c.drawString(65, h-25, "SO: "+sistema+"  Version: "+version+"  Ubicacion: "+ubicacion)
    c.drawString(65, h-50, "Tiempo de actividad antes del ultimo reinicio: "+tiempo+"hrs  Comunidad: "+comunidad+"  IP: "+ip)
    c.line(0,h-65,w,h-65)
    c.drawImage(ip+"inmulti.png",10,h-185,width=w-20,height=110)
    c.drawImage(ip+"ippackets.png",10,h-305,width=w-20,height=110)
    c.drawImage(ip+"icmpme.png",10,h-425,width=w-20,height=110)
    c.drawImage(ip+"segout.png",10,h-545,width=w-20,height=110)
    c.drawImage(ip+"datagramsin.png",10,h-665,width=w-20,height=110)
    c.save()

def generarReporte():
    lineas = leerArchivo()
    print('{color}Elige el dispositivo'.format(color=amarillo))
    i = 1
    for linea in lineas:
        ip = linea.split(" ")[0]
        print('{color}\t{i}. {ip}'.format(color=amarillo,i=i,ip=ip))
        i = i+1
    opcion = int(input().strip('\n'))
    ip = ''
    comunidad = ''
    puerto = 0
    i=0
    for linea in lineas:
        if i+1 == opcion:
            ip = linea.strip('\n').split(" ")[0]
            comunidad = linea.strip('\n').split(" ")[2]
            puerto = int(linea.strip('\n').split(" ")[3])
        i = i+1
    crearRRD(ip)
    print("{color}Ingresa la fecha y hora de inicio (DD-MM-AAAA HH:MM)".format(color=amarillo))
    inicio = input()
    inicioFormateado =time.mktime(time.strptime(inicio,"%d-%m-%Y %H:%M"))
    print("{color}Ingresa la fecha y hora de termino (DD-MM-AAAA HH:MM)".format(color=amarillo))
    fin = input()
    finFormateado =time.mktime(time.strptime(fin,"%d-%m-%Y %H:%M"))
    actualizarRRD(ip,comunidad,puerto,inicio,fin)
    graficar(ip,int(inicioFormateado),int(finFormateado))
    generarPDF(comunidad,ip,puerto)


def menu():
    print('{color}Seleccione opcion'.format(color=amarillo))
    print('{color}1. Agregar un dispositivo'.format(color=amarillo))
    print('{color}2. Eliminar un dispositivo'.format(color=amarillo))
    print('{color}3. Generar reporte'.format(color=amarillo))
    print('{color}4. Salir'.format(color=amarillo))
    opcion = input()
    if opcion == '1':
        agregarDispositivo()
    if opcion == '2':
        eliminarDispositivo()
    if opcion == '3':
        generarReporte()
    if opcion == '4':
        sys.exit(0)

while True:
    imprimirDatosDispositivos()
    menu()