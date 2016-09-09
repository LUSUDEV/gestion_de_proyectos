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
#    Modulo Desarrollado por Juventud Productiva (Victor Davila)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
##############################################################################

import json
import logging
import base64
from cStringIO import StringIO

import openerp.exceptions
from werkzeug.exceptions import HTTPException
from openerp import http,tools, api,SUPERUSER_ID
from openerp.http import request
from openerp.addons.website_apiform.controladores import panel, base_tools
from datetime import date, timedelta

_logger = logging.getLogger(__name__)

class jpv_cuentas_web(http.Controller):
    
    def mascara_montos(self,monto):
        monto='{:,.2f}'.format(monto)
        monto_actual=monto
        monto_actual=str(monto).replace('.',',')
        monto=monto_actual.split(',')
        if len(monto[1])==1:
            monto_actual=monto_actual+'0'
        return monto_actual
    
    @http.route(
            ['/jpv_cuentas'], 
            type='http', auth="user", website=True)
    def cuentas_general(self):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        mi_entidad=self.mi_entidad(uid)
        proyectos_obj = registry['jpv_cp.carga_proyecto']
        mis_cuentas=self.mis_cuentas(mi_entidad['parent_id'])
        if mis_cuentas['cuentas_data']:
            if not base_tools.users_active(uid):
                return request.redirect(base_tools.LOGIN)
            titulo=mi_entidad['entidad_data'].name \
                    +' '+mi_entidad['entidad_data'].rif+' '
            datos={'parametros':{
                            'titulo':titulo,
                            #~ 'url_boton_crear':'/usuarios/crear',
                            'template':'jpv_cuentas.tree',},
                        'mis_cuentas':mis_cuentas['cuentas_data'],
                        'mascara_montos':self.mascara_montos,
                        'proyectos':self.cant_proyectos_activos,
                    }
            return panel.panel_lista(datos)
        mensaje={
                'titulo':'Sin Cuenta',
                'mensaje':'''Disculpe NO tiene ninguna Cuenta Asignada,
                        Comuníquese con el administrador del sistema''',
                'volver':'/'
            }
        return http.request.website.render('website_apiform.mensaje', mensaje)
        
    @http.route(
        ['/mi_entidad'], 
        type='json', auth="user", website=True)
    def mi_entidad(self,uids):
        if isinstance(uids, (int, long)):
            uids = [uids]
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        ret={}
        entidades_obj = registry['jpv_ent.entidades']
        entidades_ids = entidades_obj.search(cr,
                                        SUPERUSER_ID,
                                        [('user_ids','in',uids)],
                                        context=context)
        entidades_data = entidades_obj.browse(cr,
                                        SUPERUSER_ID,
                                        entidades_ids,
                                        context=context)
        entidad_id=0
        if len(entidades_ids)==1:
            entidad_id=entidades_ids[0]
            
        user_ids=[]
        parent_id=0
        for entidad in entidades_data:
            parent_id=entidad.parent_id.id
            for user in entidad.user_ids:
                user_ids.append(user.id)
        ret={'entidad_data':entidades_data,
             'entidad_id':entidad_id,
             'parent_id':parent_id,
             'user_ids':user_ids}
        return ret
    
    
    def mis_cuentas(self,mi_entidad):
        if isinstance(mi_entidad, (int, long)):
            mi_entidad = [mi_entidad]
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        ret={}
        cuentas_obj = registry['jpv.cuentas']
        cuentas_ids = cuentas_obj.search(cr,
                                    SUPERUSER_ID,
                                    [('partner_id','in',mi_entidad)],
                                    context=context)
        cuentas_data = cuentas_obj.browse(
                                        cr,
                                        SUPERUSER_ID,
                                        cuentas_ids,
                                        context=context)
        cuenta_id=0
        for cuenta in cuentas_data:
            cuenta_id=cuenta.id
        ret={   'cuentas_data':cuentas_data,
                'cuenta_id':cuenta_id,
                }
        return ret
    
    @http.route(
            ['/jpv_cuentas/especificas/<model("jpv.cuentas"):cuenta>'], 
            type='http', auth="user", website=True)
    def cuentas_especificas(self,cuenta=None):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        mi_entidad=self.mi_entidad(uid)
        mis_cuentas=self.mis_cuentas(mi_entidad['parent_id'])
        mov_ctas_obj = registry['jpv.movimientos_cuentas']
        mov_ctas_ids=mov_ctas_obj.search(cr,
                                        SUPERUSER_ID,
                                        [('cuenta_id','=',cuenta.id)],
                                        limit=150,
                                        order='id desc',
                                        context=context)
        mov_ctas_datos=mov_ctas_obj.browse(cr,
                                        SUPERUSER_ID,
                                        mov_ctas_ids
                                        )
        proy=self.cant_proyectos_activos(mis_cuentas['cuenta_id'])
        periodos_obj = registry['jpv_plf.periodos']
        periodos_ids=periodos_obj.search(cr,
                            uid,
                            [],
                            order='id asc',
                            context=context)
        periodos_datos=periodos_obj.browse(cr, uid, periodos_ids)
        titulo=mi_entidad['entidad_data'].name \
                    +' '+mi_entidad['entidad_data'].rif+' '
        datos={'parametros':{
                        'titulo':titulo,
                        #~ 'url_boton_crear':'/usuarios/crear',
                        'template':'jpv_cuentas.especifica',},
                    'mis_cuentas':mis_cuentas['cuentas_data'],
                    'mis_movimientos':mov_ctas_datos,
                    'nombre_cuenta':cuenta.tipo_cuenta_id.name,
                    'cuenta_id':str(cuenta.id),
                    'mascara_montos':self.mascara_montos,
                    'proyectos':self.cant_proyectos_activos,
                    'periodos':periodos_datos,
                }
        return panel.panel_lista(datos)
        
    def cant_proyectos_activos(self,cuenta_id):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        ret={}
        proyectos_obj = registry['jpv_cp.carga_proyecto']
        proyectos_ids=proyectos_obj.search(cr,
                                        SUPERUSER_ID,
                                        [('state','in',['aprobado']),
                                        ('cuenta_id','=',cuenta_id)],
                                        context=context)
        return proyectos_ids

    @http.route(
        ['/jpv_cuentas/movimientos'],
        type='json', auth='user', website=True)
    def consulta_ctas_movimientos(self,**post):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        res=[]
        nombre_proyecto=[]
        proyectos_obj = registry['jpv_cp.carga_proyecto']   
        proyectos_ids=proyectos_obj.search(cr,
                                SUPERUSER_ID,
                                [('correlativo','like',post['key']),
                                ('cuenta_id','=',int(post['cuenta_id']))])
        proyectos_data=proyectos_obj.browse(cr,SUPERUSER_ID,proyectos_ids)
        for proyecto in proyectos_data:
            res.append({
                        'id2':proyecto.id,
                        'name2':proyecto.correlativo,
                        })
        mov_ctas_obj = registry['jpv.movimientos_cuentas']
        if post['code']==13:
            ret =  {'modal':{
                    'titulo':'<strong>Aviso.</strong>',
                    'cuerpo':'''<h4 class="text-danger" >
                                Debe seleccionar el registro del
                                Proyecto que va a consultar...</h4>
                                ''' ,
                            },
                    }
            return ret
        ret =  {'datos':res,'code': post['code'],'cuenta_id':int(post['cuenta_id'])}
        return ret
    
    @http.route(
        ['/jpv_cuentas/movimientos/seleccion'],
        type='json', auth='user', website=True)
    def consulta_cta_mov_seleccion(self,**post):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        res=[]
        mov_ctas_obj = registry['jpv.movimientos_cuentas']
        cta_mov_ids=mov_ctas_obj.search(cr,
                            SUPERUSER_ID,
                            [('name','=',post['name']),
                            ('cuenta_id','=',int(post['cuenta_id']))],
                            context=context)
        cta_mov_data=mov_ctas_obj.browse(cr, SUPERUSER_ID, cta_mov_ids)
        for movimientos in cta_mov_data:
                monto_egreso=self.mascara_montos(movimientos.monto_egreso)
                monto_ingreso=self.mascara_montos(movimientos.monto_ingreso)
                monto_saldo=self.mascara_montos(movimientos.monto_saldo)
                res.append({
                        'id':movimientos.id,
                        'fecha_movimiento':movimientos.fecha_movimiento,
                        'accion':movimientos.accion,
                        'name':movimientos.name,
                        'monto_egreso':monto_egreso,
                        'monto_ingreso':monto_ingreso,
                        'monto_saldo':monto_saldo,
                        })
        ret =  {'datos':res,'code': post['id'],'cuenta_id':int(post['cuenta_id'])}
        return ret
    
    @http.route(
            ['/jpv_cuentas/movimientos/bus_avanzada'], 
            type='json', auth="user", website=True)
    def busqueda_movimientos_cuentas_avanzada(self,**post):
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        res=[]
        mov_ctas_obj = registry['jpv.movimientos_cuentas']
        where=[('cuenta_id','=',int(post['cuenta_id2']))]
        if post['cta_fecha_inicial'] and post['cta_fecha_final']=='':
            d,m,a=post['cta_fecha_inicial'].split('-')
            fecha_inicio = date(int(a),int(m),int(d))
            where.append(('fecha_movimiento','=',fecha_inicio))
        if post['cta_fecha_final'] and post['cta_fecha_inicial']=='':
            d,m,a=post['cta_fecha_final'].split('-')
            fecha_fin = date(int(a),int(m),int(d))
            where.append(('fecha_movimiento','=',fecha_fin))
        if post['cta_fecha_inicial'] and post['cta_fecha_final']:
            d,m,a=post['cta_fecha_inicial'].split('-')
            fecha_inicio = date(int(a),int(m),int(d))
            d,m,a=post['cta_fecha_final'].split('-')
            fecha_fin = date(int(a),int(m),int(d))
            where.append(('fecha_movimiento','>=',fecha_inicio))
            where.append(('fecha_movimiento','<=',fecha_fin))
        
        if post['monto_egreso'] and post['monto_egreso2']=='':
            monto_egreso=str(post['monto_egreso']).replace('.','')
            monto_egreso=monto_egreso.replace(',','.')
            where.append(('monto_egreso','=',monto_egreso))
        
        if post['monto_egreso2'] and post['monto_egreso']=='':
            monto_egreso2=str(post['monto_egreso2']).replace('.','')
            monto_egreso2=monto_egreso2.replace(',','.')
            where.append(('monto_egreso','=',monto_egreso2))
        
        if post['monto_egreso'] and post['monto_egreso2']:
            monto_egreso=str(post['monto_egreso']).replace('.','')
            monto_egreso=monto_egreso.replace(',','.')
            monto_egreso2=str(post['monto_egreso2']).replace('.','')
            monto_egreso2=monto_egreso2.replace(',','.')
            where.append(('monto_egreso','>=',monto_egreso))
            where.append(('monto_egreso','<=',monto_egreso2))
        
        if post['monto_ingreso'] and post['monto_ingreso2']=='':
            monto_ingreso=str(post['monto_ingreso']).replace('.','')
            monto_ingreso=monto_ingreso.replace(',','.')
            where.append(('monto_ingreso','=',monto_ingreso))
        
        if post['monto_ingreso2'] and post['monto_ingreso']=='':
            monto_ingreso2=str(post['monto_ingreso2']).replace('.','')
            monto_ingreso2=monto_ingreso2.replace(',','.')
            where.append(('monto_ingreso','=',monto_ingreso2))
        
        if post['monto_ingreso'] and post['monto_ingreso2']:
            monto_ingreso=str(post['monto_ingreso']).replace('.','')
            monto_ingreso=monto_ingreso.replace(',','.')
            monto_ingreso2=str(post['monto_ingreso2']).replace('.','')
            monto_ingreso2=monto_ingreso2.replace(',','.')
            where.append(('monto_ingreso','>=',monto_ingreso))
            where.append(('monto_ingreso','<=',monto_ingreso2))
        cta_mov_ids=mov_ctas_obj.search(cr,
                            SUPERUSER_ID,
                            where,
                            order='id desc',
                            context=context)
        cta_mov_data=mov_ctas_obj.browse(cr, SUPERUSER_ID, cta_mov_ids)
        if cta_mov_data:
            for movimientos in cta_mov_data:
                monto_egreso=self.mascara_montos(movimientos.monto_egreso)
                monto_ingreso=self.mascara_montos(movimientos.monto_ingreso)
                monto_saldo=self.mascara_montos(movimientos.monto_saldo)
                res.append({
                        'id':movimientos.id,
                        'fecha_movimiento':movimientos.fecha_movimiento,
                        'accion':movimientos.accion,
                        'name':movimientos.name,
                        'monto_egreso':monto_egreso,
                        'monto_ingreso':monto_ingreso,
                        'monto_saldo':monto_saldo,
                        })
            ret =  {'datos':res}
            return ret
        ret =  {'modal':{
                    'titulo':'<strong>Busqueda sin resultado.</strong>',
                    'cuerpo':'''<h4 class="text-danger" >
                                La busqueda que realizo no 
                                obtuvo ningún resultado...</h4>
                                ''' ,
                            },
                    }
        return ret
            
    @http.route(
            ['/jpv_cuentas/periodo/imprimir'], 
            type='http', auth="user", website=True)
    def jpv_imprimir_periodos(self, **post):
        hoy=date.today()
        registry = http.request.registry
        cr, uid, context = request.cr, request.uid, request.context
        mi_entidad=self.mi_entidad(uid)
        mis_cuentas=self.mis_cuentas(mi_entidad['parent_id'])
        nombre_entidad=mi_entidad['entidad_data'].name
        rif_entidad=mi_entidad['entidad_data'].rif
        periodos_obj = registry['jpv_plf.periodos']
        asignacion_recurso_obj = registry['jpv_asr.recurso']
        movimiento_cuenta_obj = registry['jpv.movimientos_cuentas']
        periodo_ids=[]
        periodos_post=panel.dict_keys_startswith(post,'periodo_')
        for periodo in periodos_post:
            periodo_ids.append(int(periodos_post[periodo]))
        asignacion_recurso_ids=asignacion_recurso_obj.search(
                                        cr,uid,
                                        [('periodo_id','in',periodo_ids),
                                        ('res_partner_id','=',mi_entidad['parent_id'])],)
        asignacion_recurso_datos=asignacion_recurso_obj.browse(cr, uid, asignacion_recurso_ids)
        print asignacion_recurso_datos
        periodos_datos=periodos_obj.browse(cr, uid, periodo_ids)
        fecha_fin=''
        for periodo in periodos_datos:
            print 'periodo.fecha_fin'
            a,m,d=periodo.fecha_fin.split('-')
            fecha_fin = date(int(a),int(m),int(d))
        movimiento_cuenta_ids=movimiento_cuenta_obj.search(cr,uid,
                                                    [
                                                    ('cuenta_id','=',mis_cuentas['cuenta_id'])],
                                                    limit=1,order='id desc'
                                                    )
        print 'movimiento_cuenta_ids'
        print movimiento_cuenta_ids
        movimiento_cuenta_datos=movimiento_cuenta_obj.browse(cr,uid,movimiento_cuenta_ids)
        reportname='jpv_cuentas.id_cta_saldo_ird_report_qweb'
        docids=[]
        valores={'asignacion_recurso_datos':asignacion_recurso_datos,
                    'movimiento_cuenta_datos':movimiento_cuenta_datos,
                    'nombre_entidad':nombre_entidad,
                    'rif_entidad':rif_entidad}
        pdf = request.registry['report'].get_pdf(cr, uid, docids, reportname, data=valores, context=context)
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        response=request.make_response(pdf, headers=pdfhttpheaders)
        response.headers.add('Content-Disposition', 'attachment; filename=%s.pdf;' % reportname)
        return response
    
