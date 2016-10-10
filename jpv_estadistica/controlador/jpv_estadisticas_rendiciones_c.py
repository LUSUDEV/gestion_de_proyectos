# -*- coding: utf-8 -*-

import csv, operator
from openerp.addons.web.controllers import main
from cStringIO import StringIO
from openerp.http import request
from openerp import http,tools, api,SUPERUSER_ID

class jpv_estadisticas_rendiciones(http.Controller):

	head_csv=['Código','Nombre del Proyecto','Monto','Estado','Motivo']

	
        #~ Ruta de grafica de torta de estadistica Rendiciones, la que tiene de header Total de Proyectos Rendidos xxx
    @http.route(
            ['/eptEstadisticasRendiciones'], 
            type='json', auth="public", website=True)
    def proyectos_rendir(self,**post):
        registry = http.request.registry
        cr=http.request.cr
        uid=http.request.uid
        context = http.request.context
        condicion=""
        if int(post['periodo_id'])>0:
            condicion=" p.periodo_id=%s and" % post['periodo_id']
        if int(post['ciclo_id'])>0:
            condicion=" p.periodo_id=%s and p.ciclo_id=%s and" % (post['periodo_id'],post['ciclo_id'])
        if int(post['estado_id'])>0:
            condicion=condicion+" p.estado_id=%s and" % post['estado_id']
        if int(post['entidad_id'])>0:
            condicion=condicion+" p.partner_id=%s and" % post['entidad_id']
            
        cr.execute("""select proyecto.id as proyecto_id,
                      proyecto.correlativo as correlativo,
                      rendicion.id as rendicion_id
                      from jpv_cp_carga_proyecto as proyecto
                      where proyecto.state='aprobado' and '%s' active=true""" % condicion)



        respuesta=cr.dictfetchone()
        return {'datos':respuesta}
        
