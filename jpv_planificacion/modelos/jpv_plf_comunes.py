# -*- coding: utf-8 -*-
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import *

#~ Este metodo valida los siguientes casos:
    #~ 1- Que la fecha final no sea menor a la fecha inicial.
    #~ 2. Que la fecha inicial no sea igual a la fecha final.
    #~ 3. Valida que la fecha inicial exista antes de seleccionar la fecha final.



def validar_fecha(fecha_inicio, fecha_fin):
        fechas={} 
        mensaje={}
        if fecha_inicio and fecha_fin:
            if cmp(fecha_inicio,fecha_fin)==1:
                fechas={
                    'fecha_fin':'',
                        }
                mensaje={
                    'title':('Error de fecha'),
                    'message':('La fecha de inicio no puede ser mayor\
                                a la fecha final'),
                    }
            if cmp(fecha_inicio,fecha_fin)==0:
                fechas={
                    'fecha_fin':'',
                        }
                mensaje={
                    'title':('Error de fecha'),
                    'message':('La fecha de inicio no puede ser igual\
                                a la fecha final'),
                    }
        else:
            if fecha_fin:
                fechas={
                    'fecha_fin':'',
                        }
                mensaje={
                        'title':('Error de fecha'),
                        'message':('Debe seleccionar una fecha de inicio'),
                        }
        return {
            'warning':mensaje,
            'value':fechas
                }
                
#~ este metodo limpia el campo de la fecha final si la fecha inicial cambia.

def limpiar_campo_fecha(fecha_inicio):
    fecha={}
    if fecha_inicio:
        fecha={
            'fecha_fin':''
            }
    return {
        'value':fecha
            }
            

#~ Metodo para el calculo de tiempo entre dos fechas dadas

def calculo_tiempo(fecha_inicio,fecha_fin):
    anos="Años"
    meses="Meses"
    dias="Días"
    duracion_proyecto=''
    if fecha_inicio and fecha_fin:
        ai,mi,di=fecha_inicio.split('-')
        fecha_inicio = date(int(ai),int(mi),int(di))
        af,mf,df=fecha_fin.split('-')
        fecha_fin = date(int(af),int(mf),int(df))
        duracion=relativedelta(fecha_fin, fecha_inicio)
        if duracion.years==1 or duracion.years==0 :
            anos="Año"
        if duracion.months==1 or duracion.months==0 :
            meses="Mes"
        if duracion.days==1 or duracion.days==0 :
            dias="Día"
        if duracion.years+duracion.months+duracion.days>0:
            duracion_proyecto=" %s %s; %s %s; %s %s  " % (duracion.years,
                                                          anos,
                                                          duracion.months,
                                                          meses,
                                                          duracion.days+1,
                                                          dias)
    return duracion_proyecto


#~ Metodo que recibe una lista con argumentos (enteros) y genera un total

def generar_total(lista_numeros):
    total=0
    for n in lista_numeros:
        total+=n
    return total

