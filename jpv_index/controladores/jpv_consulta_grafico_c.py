# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#    
#    Modulo Desarrollado por CFG (Hector Andrade)
#
#############################################################################

import json
import logging
import base64
from cStringIO import StringIO

import openerp.exceptions
from werkzeug.exceptions import HTTPException
from openerp import http,tools, api,SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_apiform.controladores import panel, base_tools
from datetime import datetime, date, time, timedelta
from openerp.addons.jpv_usuarios.controladores.jpv_use_users_c import jpv_users as jpv_usuarios

class jpv_cp_carga_proyecto_controlador(http.Controller):

    @http.route('/proyecto/consulta/grafica',type='json', auth="public", website=True)
    def consulta_proyecto (self, **kw):
        uid=http.request.uid
        registry=request.registry
        cr=request.cr
        #~ print cr


        entidad_data=jpv_usuarios().mi_entidad(uid)
        #~ print entidad_data['entidad_id']
        #~ print entidad_data['entidad_data'].parent_id
        
        #~ print entidad_data


        proyecto_obj=registry['jpv_cp.carga_proyecto']
        rendicion_obj=registry['jpv_rnd.rendicion']
        
        cr.execute("select  (SELECT COUNT(state) aprobado FROM jpv_cp_carga_proyecto WHERE state='aprobado' and partner_id = %s) as aprobado,"\
            "(SELECT COUNT(state) evaluacion FROM jpv_cp_carga_proyecto WHERE state='evaluacion' and partner_id = %s) as evaluacion,"\
            "(SELECT COUNT(state) culminado FROM jpv_cp_carga_proyecto WHERE state='culminado' and partner_id = %s) as culminado,"\
            "(SELECT COUNT(state) cancelado FROM jpv_cp_carga_proyecto WHERE state='cancelado' and partner_id = %s) as cancelado,"\
            "(SELECT COUNT(state) carga FROM jpv_cp_carga_proyecto WHERE state='carga' and partner_id = %s) as carga" % (entidad_data['entidad_data'].parent_id.id, entidad_data['entidad_data'].parent_id.id, entidad_data['entidad_data'].parent_id.id, entidad_data['entidad_data'].parent_id.id, entidad_data['entidad_data'].parent_id.id));
        
        lista_counts1=list (cr.fetchall()[0])
        #~ print lista_counts1        
        #~ print lista_counts1
        
            
        cr.execute("select  (SELECT COUNT(estatus_proyecto) Sin_iniciar FROM jpv_rnd_rendicion a left join jpv_cp_carga_proyecto b on b.id=a.proyecto_id WHERE estatus_proyecto='Sin iniciar' and b.state <> 'cancelado' and b.partner_id = %s) as Sin_iniciar,"\
            "(SELECT COUNT(estatus_proyecto) En_ejecucion FROM jpv_rnd_rendicion a left join jpv_cp_carga_proyecto b on b.id=a.proyecto_id WHERE estatus_proyecto='En ejecucion' and b.partner_id = %s) as En_ejecucion,"\
            "(SELECT COUNT(estatus_proyecto) Paralizado FROM jpv_rnd_rendicion a left join jpv_cp_carga_proyecto b on b.id=a.proyecto_id WHERE estatus_proyecto='Paralizado' and b.partner_id = %s) as Paralizado,"\
            "(SELECT COUNT(estatus_proyecto) Culminado FROM jpv_rnd_rendicion a left join jpv_cp_carga_proyecto b on b.id=a.proyecto_id WHERE estatus_proyecto='Culminado' and b.partner_id = %s) as Culminado"% (entidad_data['entidad_data'].parent_id.id, entidad_data['entidad_data'].parent_id.id, entidad_data['entidad_data'].parent_id.id, entidad_data['entidad_data'].parent_id.id));

            
        lista_counts2=list (cr.fetchall()[0])
        #~ print lista_counts2        
        #~ print lista_counts2
        
        cr.execute("select a.avance_financiero, a.avance_fisico_porc, b.monto_proyecto from jpv_rnd_rendicion a left join jpv_cp_carga_proyecto b on a.proyecto_id=b.id where b.state <> 'cancelado' and b.partner_id = %s" % (entidad_data['entidad_data'].parent_id.id));
        
        
        lista_counts3=list (cr.fetchall())
        #~ print lista_counts3
        avance_financiero_list=[]
        avance_fisico_list=[]
        for fila in lista_counts3:
            #~ print fila[0]
            #~ print fila[2]
            if fila[0] != None:
                monto_gastado=fila[0]
                monto_gastado=monto_gastado.replace(".","")
                monto_gastado=monto_gastado.replace(",",".")
                monto_gastado=float(monto_gastado)
                
            else:
                monto_gastado=float(0.0)    
            if fila[1] != None:
                avance_fisico=fila[1]
                avance_fisico=avance_fisico.replace("%","")
                avance_fisico=float(avance_fisico)

                
            else:
                avance_fisico=float(0.0)    
            #~ print monto_gastado
            avance_financiero_porcentaje=(monto_gastado*100)/fila[2]
            avance_financiero_porcentaje= float(str(unicode("%.2f" % avance_financiero_porcentaje)))
            
            avance_financiero_list.append(avance_financiero_porcentaje)
            avance_fisico_list.append(avance_fisico)
            
        #~ print 'lista avance financiero'
        #~ print avance_financiero_list
        #~ print 'lista avance fisico'
        #~ print avance_fisico_list
        
        sumatoria_financiero = 0
        i=0
        for i in range(0, len(avance_financiero_list)):
            #~ print avance_financiero_list[i]
            sumatoria_financiero = sumatoria_financiero + avance_financiero_list[i]
        i = i + 1
        total_financiero = sumatoria_financiero / i
        total_financiero = float(str(unicode("%.2f" % total_financiero)))
       
        #~ print "Total es financiero " + str(total_financiero) + " i vale " + str(i)
        
        sumatoria_fisico = 0
        for i in range(0, len(avance_fisico_list)):
            #~ print avance_fisico_list[i]
            sumatoria_fisico = sumatoria_fisico + avance_fisico_list[i]
        i = i + 1
        total_fisico = sumatoria_fisico / i
        total_fisico = float(str(unicode("%.2f" % total_fisico)))
       
        #~ print "Total es fisico " + str(total_fisico) + " i vale " + str(i)
        
        
        #~ return total
       
        return {'cant_proy_aprobados':{'data':[lista_counts1[0]],
                                       'name':'Aprobados'},
                'cant_proy_evaluacion':{'data':[lista_counts1[1]],
                                        'name':'Evaluacion'},
                'cant_proy_culminado':{'data':[lista_counts1[2]],
                                        'name':'Culminados'},
                'cant_proy_cancelado':{'data':[lista_counts1[3]],
                                        'name':'Cancelados'},
                'cant_proy_carga': {'data':[lista_counts1[4]],
                                    'name':'Carga'},
                'cant_proy_sin_iniciar':lista_counts2[0],
                'cant_proy_ejecucion':lista_counts2[1],
                'cant_proy_paralizado':lista_counts2[2],
                'cant_proy_culminado_r':lista_counts2[3],
                
                #~ 'json_data':[{'data':[['Avance financiero',total_financiero],
                                     #~ ['Avance Fisico',total_fisico]]}]
                'cant_total_financiero':{'data':[total_financiero],
                                       'name':'Avance financiero'},
                'cant_total_fisico':{'data':[total_fisico],
                                        'name':'Avance Fisico'},

 
                }


