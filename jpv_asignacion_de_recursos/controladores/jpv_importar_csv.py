# -*- coding: utf-8 -*-
import base64
import werkzeug
import werkzeug.urls
from openerp.osv import fields, osv
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request, STATIC_CACHE
from openerp.tools.translate import _
from openerp.addons.website.models.website import slug
from openerp.addons.web.controllers.main import login_redirect
from datetime import datetime,date
import time 
import logging

logger = logging.getLogger(__name__)



class importar_asignacion(http.Controller):
    
    
    @http.route('/asignacion_recursos/importar_csv', type='json', auth='public', website=True)
    def importar_asignacion(self, **values):
        registry = http.request.registry
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        asignacion_obj = registry['jpv_asr.recurso_general']
        asignacion_id = asignacion_obj.create(cr,SUPERUSER_ID, values, context)
        return asignacion_id
    
    
    
    @http.route('/asignacion_recursos/exportar', type='http', auth='public', website=True)
    def exportar_lista(self, **values):
        lista_partners_ids = values['partner_ids'].split(',')
        registry = http.request.registry
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        asignacion_obj = registry['jpv_asr.recurso_general']
        asignacion_id = asignacion_obj.exportar_csv(cr,SUPERUSER_ID, lista_partners_ids, values['token'], context=None)
        return asignacion_id
           
        
   
