# -*- coding: utf-8 -*-
########################################################################
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
#    Modulo Desarrollado por Juventud Productiva (Jose Mancilla)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
#############################################################################

import openerp
import requests
from openerp.addons.web.controllers import main
from openerp import http
from openerp import tools, api
from openerp.models import fix_import_export_id_paths
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _
from openerp.http import request, serialize_exception as _serialize_exception
from imaplib import IMAP4
from imaplib import IMAP4_SSL
from poplib import POP3
from poplib import POP3_SSL
import urllib
from datetime import datetime, date, time, timedelta
from dateutil.relativedelta import *

class jpv_asr_rescurso_general(osv.osv):
    _name='jpv_asr.recurso_general'
    _rec_name='descripcion'
    
    tipo_cuenta_id={}
    list_res_partner_ids=[]
    
    
    _columns = {
    
        'tipo_cuenta':fields.many2one('jpv.tipo_cuentas','Tipo de Cuenta'),
        'monto_asignar':fields.float(
                        'Monto General Asignar',
                        required=True,
                        help='Monto General que se va asiganar.',
                        ),
        'descripcion':fields.text('Descripción'),
        
        'asignacion_recursos_line':fields.one2many(
                    'jpv_asr.recurso',
                    'asignacion_de_recurso_line_id',
                    'Asignaciones'),
        
        'state':fields.selection([
            ('Borrador', 'Borrador'),
            ('Asignado', 'Asignado'),
            ], 'Status', readonly=True, copy=False, help="estado del Ird", select=True),
    
        
        'periodo_id': fields.many2one(
                        'jpv_plf.periodos', 
                        'Periodo',
                        required=True),
    }
    
    _defaults={
        'state': 'Borrador',
    }
    
    def valor_monto_asignar(self,cr,uid,ids,asg_gen_recurso_id,context=None):
        """Metodo on_change que obtiene el valor del monto en la asignación
        genreal de recursos y """
        res={}
        if not asg_gen_recurso_id:
            res={'monto_asignar':''}
        asig_gen_rec_obj=self.pool.get('jpv_fto.asignacion_general_recursos')
        if asg_gen_recurso_id:
            for mont_asignar in asig_gen_rec_obj.browse(cr,uid,asg_gen_recurso_id):
                monto='%.2f' % mont_asignar.monto_asignar
                res={'monto_asignar':str(monto)}
        return {'value':res}
    
    
    def pre_validar_asignacion(self,cr,uid,ids,context=None):
        """Metodo que realiza una pre validación para la asignacion general de
        recursos la cual valida que existan registros en el One2Many que ningún 
        monto este en Cero o negativo y que el Monto General Asiganr sea igual
        a la suma de los montos ingresados en el One2Many """
        movimientos_obj=self.pool.get('jpv.movimientos_cuentas')
        monto=0
        for asignacion in self.browse(cr, uid, ids):
            if not len(asignacion.asignacion_recursos_line):
                raise osv.except_osv(
                    ('Error!'),
                    (u'No ha seleccionado ninguna Entidad o Institución.'))
            for asignacion_line in asignacion.asignacion_recursos_line:
                monto=monto+asignacion_line.monto
                if asignacion_line.monto <= 0:
                    nombre_partner=asignacion_line.res_partner_id.name
                    raise osv.except_osv(
                        ('Error!'),
                        (u'El monto para la asignacion de '+nombre_partner+' \
                        es incorrecto. El monto a asignar para cada Entidad \
                        o Institución debe ser mayor a Cero o no puede \
                        ser Negativo.'))
        monto=float('%.2f' % monto)
        if asignacion.monto_asignar != monto:
            raise osv.except_osv(
                    ('Error!'),
                    (u'La suma Total del Monto de las Entidades (%s) debe \
                    ser exactamente igual al Monto General Asignar (%s), \
                    poder poder validar el registro, '
                    % ((monto,asignacion.monto_asignar))))
        return True
    
    def validar_asignacion(self,cr,uid,ids,context=None):
        movimientos_obj=self.pool.get('jpv.movimientos_cuentas')
        asignacion_data=self.browse(cr, uid, ids)
        monto=0
        arreg=[]
        for r in asignacion_data:
            if not len(r.asignacion_recursos_line):
                raise osv.except_osv(
                    ('Error!'),
                    (u'No ha seleccionado ninguna Entidad o Institución.'))
            nro_movimientos=len(r.asignacion_recursos_line)
            movimientos_ids=[]
            for i in r.asignacion_recursos_line:
                arreg.append(i.id)
                monto=monto+i.monto
                if not i.monto > 0:
                    nombre_partner=u''+i.res_partner_id.name
                    raise osv.except_osv(
                        ('Error!'),
                        (u'El monto para la asignacion de '+nombre_partner+' es incorrecto'
                         u'\nEl monto a asignar para cada Entidad o Institución , \
                         debe ser mayor a 0'))
                
                #~ busco el id de la cuenta
                cuenta_id=movimientos_obj.partner_id_tipo_cuenta_id(cr,uid,i.res_partner_id.id,i.tipo_cuenta.id)
                #~ genero el movimiento de ingreso por asignacion pasandole la cuenta_id el monto y la descripcion
                movimiento_id=movimientos_obj.movimiento_ingreso(cr,uid,cuenta_id[0], 
                                                            i.monto, 
                                                            'Asignacion de Recursos', 
                                                            i.descripcion, 
                                                            i._name, i.id,
                                                            r.periodo_id.id )
                if not movimiento_id['movimiento_id_ingreso']:
                    print 'Error Transaccion Fallida'
                    movimientos_obj.eliminar_movimiento(movimientos_ids,'Transaccion Fallida',i.descripcion,r.periodo_id.id)
                    return False
                movimientos_ids.append([i.id,movimiento_id['movimiento_id_ingreso']])
            #~ If que controla que los montos de asignar general y la suma de  
            #~ los montos de las entidades que estos sean iguales para poder  
            #~ validar las asignaciones se formatean los montos para controlar
            #~ que si son base 10 este se coloque en numero entero y luego se 
            #~ pasa a string para controlar y validar los valores de los montos
            monto='%.2f' % monto
            if str('%.2f' % r.monto_asignar) != str(monto):
                raise osv.except_osv(
                        ('Error!'),
                        (u'La suma Total del Monto de las Entidades (%s) debe \
                        ser exactamente igual al Monto General Asignar (%s), \
                        poder poder validar el registro, '
                        % ((monto,r.monto_asignar))))
            if len(movimientos_ids)==len(r.asignacion_recursos_line):
                for rr in movimientos_ids:
                    write=self.pool.get('jpv_asr.recurso').write(cr,uid,rr[0],{'transaccion_id':rr[1]},context)
                write_id=self.write(cr,uid,ids,{'state':'Asignado'},context)
                    
            else:
                print 'Error Transaccion Fallida'
                movimientos_obj.eliminar_movimiento(movimientos_ids,'Transaccion Fallida',i.descripcion,r.periodo_id.id)
                return False
        return write_id
        
    def calculo_monto_mensual(self,cr,uid,ids,
                                        asg_gen_recurso_datos,
                                        asignacion_recursos_line_datos,
                                        context=None):
        montos_cau_pag_obj=self.pool.get('jpv_fto.montos_causado_pagado')
        asig_gral_recurso_obj=self.pool.get('jpv_fto.asignacion_general_recursos')
        mov_cta_gen_cfg_obj=self.pool.get('jpv_fto.movimientos_cuenta_general_cfg')
        cta_gen_cfg_obj=self.pool.get('jpv_fto.cuenta_general_cfg')
        cta_gen_cfg_id=cta_gen_cfg_obj.search(cr,uid,
                                [('name','=','CONSEJO FEDERAL DE GOBIERNO')],
                                limit=1,order="id desc")
        cta_gen_cfg_datos=cta_gen_cfg_obj.browse(cr,uid,cta_gen_cfg_id)
        monto_saldo=0.00
        for cta_general in cta_gen_cfg_datos:
            if not cta_general.mvto_gen_cuenta_ids:
                monto_saldo=asg_gen_recurso_datos.monto_asignar
            for mvto_general in cta_general.mvto_gen_cuenta_ids:
                monto_saldo=asg_gen_recurso_datos.monto_asignar+mvto_general.monto_saldo
        mov_cta_esp_cfg_obj=self.pool.get('jpv_fto.movimientos_cuenta_especificos_cfg')
        mov_cta_esp_cfg_ids=mov_cta_esp_cfg_obj.search(cr,uid,
                                [],
                                limit=1,order="id desc")
        mov_cta_esp_cfg_datos=mov_cta_esp_cfg_obj.browse(cr,uid,mov_cta_esp_cfg_ids)
        monto_saldo_especifico=0.00
        if not mov_cta_esp_cfg_datos:
            monto_saldo_especifico=asg_gen_recurso_datos.monto_asignar
        for cta_especifica in mov_cta_esp_cfg_datos:
            monto_saldo_especifico=asg_gen_recurso_datos.monto_asignar+cta_especifica.monto_saldo
        hoy=date.today()
        montos_cau_pag_line=[]
        mvto_esp_cta_line=[]
        mvto_esp_cta_valores=[]
        cta_gen_cfg_valores=[]
        mvto_esp_cta_valores={'state':'comprometido'}
        for asig_rec_line in asignacion_recursos_line_datos:
            recorre=0
            while recorre < int(asg_gen_recurso_datos.valor_calculo_fechas):
                a,m,d=asg_gen_recurso_datos.fecha_inicio.split('-')
                fecha_inicio = date(int(a),int(m),int(d))
                fecha_inicio=fecha_inicio+relativedelta(months=+recorre)
                fecha_inicio2 = fecha_inicio.strftime("%B")
                montos_cau_pag_line.append([0,False,
                            {'state': 'borrador', 
                            'mes':str(fecha_inicio2),
                            'partner_id': asig_rec_line.res_partner_id.id,
                            'monto':float(asig_rec_line.monto/int(asg_gen_recurso_datos.valor_calculo_fechas)),
                            'asignacion_general_id':False}])
                recorre += 1
        mvto_esp_cta_line.append([0,False,
                        {'accion':u'Asignación de Recurso',
                        'name': asg_gen_recurso_datos.name,
                        'fecha_movimiento':hoy,
                        'monto_credito':asg_gen_recurso_datos.monto_asignar,
                        'monto_saldo':monto_saldo_especifico,
                        'periodo_id':asg_gen_recurso_datos.periodo_id.id,
                        'cuenta_especifica_id':False,}])
        cta_gen_cfg_valores.append([0,False,
                        {'accion':u'Asignación de Recurso',
                        'name': asg_gen_recurso_datos.name,
                        'fecha_movimiento':hoy,
                        'monto_credito':asg_gen_recurso_datos.monto_asignar,
                        'monto_saldo':monto_saldo,
                        'cuenta_general_id':False}])
        mvto_esp_cta_valores.update({'mvto_especifico_cuenta_ids': mvto_esp_cta_line})
        mvto_esp_cta_valores.update({'montos_causado_pagado_ids': montos_cau_pag_line})
        asig_gral_recurso_id=asig_gral_recurso_obj.write(cr,uid,
                                    [asg_gen_recurso_datos.id],
                                    mvto_esp_cta_valores)
        asig_gral_recurso_obj.monto_borrador_causado(cr,uid,asig_gral_recurso_id)
        cta_gen_cfg_obj.write(cr,uid,
                                cta_gen_cfg_id,
                                {'mvto_gen_cuenta_ids':cta_gen_cfg_valores})
        return True
    
    def monto_mantenimiento(self,cr,uid,ids,
                                        asg_gen_recurso_datos,
                                        asignacion_recursos_line_datos,
                                        context=None):
        jpv_entidades_obj=self.pool.get('jpv_ent.entidades')
        resultado_monto_porc=0.00
        for asig_rec_line in asignacion_recursos_line_datos:
            partner_id=asig_rec_line.res_partner_id.id
            entidad_id=jpv_entidades_obj.search(cr,uid,
                                            [('parent_id','=',partner_id)])
            monto_porcentaje=int(asg_gen_recurso_datos.periodo_id.porc_manten)
            resultado_monto_porc=float((asig_rec_line.monto*monto_porcentaje)/100)
            jpv_entidades_datos=jpv_entidades_obj.browse(cr,uid,entidad_id)[0]
            monto_disp_mant=jpv_entidades_datos.monto_disp_mantenimiento+resultado_monto_porc
            jpv_entidades_obj.write(cr,uid,
                                entidad_id[0],
                                {'monto_disp_mantenimiento':monto_disp_mant})
        return True
    
    def onchange_tipo_cuenta(self,cr,uid,ids,tipo_cuenta,context=None):
        self.tipo_cuenta_id=tipo_cuenta
        domain=self.pool.get('jpv_asr.recurso').onchange_tipo_cuenta(cr, uid, ids, tipo_cuenta, context)
        return {'domain': domain}
    
    def onchange_res_partner(self, cr, uid, ids, asignacion_recursos_line,tipo_de_cuenta, context=None):
        self.tipo_cuenta_id=tipo_de_cuenta
        self.list_res_partner_ids=[]
        if asignacion_recursos_line:
            for i in asignacion_recursos_line:
                if 'res_partner_id' in i[2]:
                    self.list_res_partner_ids.append(i[2]['res_partner_id'])
                else:
                    for r in i[2]:
                        self.list_res_partner_ids.append(self.pool.get('jpv_asr.recurso').browse(cr,uid,r).res_partner_id.id)
        self.list_res_partner_ids=list(set(self.list_res_partner_ids))
        return True
    
        
        
    def exportar_csv(self,cr,uid, ids, token, context=None):
        partners_ids=[]
        for i in ids:
            partners_ids.append(int(i))
        data = self.pool.get('res.partner').read(cr,uid,partners_ids,['name'])
        header=['Asignaciones / Entidad o Institucion',
                'Asignaciones / Monto a asignar']
        list_rows=[]
        for i in data:
            lista=[]
            lista.append(i['name'])
            lista.append('')
            list_rows.append(lista)
        export_obj=main.CSVExport()
        return http.HttpRequest(request.httprequest).make_response(export_obj.from_data(header, list_rows),
            headers=[('Content-Disposition',
                            main.content_disposition(export_obj.filename(self._name))),
                     ('Content-Type', export_obj.content_type)],
                    cookies={'fileToken': token})

        
    def load(self, cr, uid, fields, data, model_id=False, context=None):
        """
            Se sobrescribe el metodo load de res models
        """
        cr.execute('SAVEPOINT model_load')
        messages = []
        
        fields = map(fix_import_export_id_paths, fields)
        ModelData = self.pool['ir.model.data'].clear_caches()
        fg = self.fields_get(cr, uid, context=context)
        
        mode = 'init'
        current_module = ''
        noupdate = False

        ids = []
        for id, xid, record, info in self._convert_records(cr, uid,
                self._extract_records(cr, uid, fields, data,
                                      context=context, log=messages.append),
                context=context, log=messages.append):
            try:
                cr.execute('SAVEPOINT model_load_save')
            except psycopg2.InternalError, e:
                # broken transaction, exit and hope the source error was
                # already logged
                if not any(message['type'] == 'error' for message in messages):
                    messages.append(dict(info, type='error',message=
                        u"Unknown database error: '%s'" % e))
                break
            
            if model_id:
                    ids=self.write(cr,uid,model_id,record)
            
            else: 
                try:
                    
                    ids.append(ModelData._update(cr, uid, self._name,
                         current_module, record, mode=mode, xml_id=xid,
                         noupdate=noupdate, res_id=id, context=context))
                    cr.execute('RELEASE SAVEPOINT model_load_save')
                except psycopg2.Warning, e:
                    messages.append(dict(info, type='warning', message=str(e)))
                    cr.execute('ROLLBACK TO SAVEPOINT model_load_save')
                except psycopg2.Error, e:
                    messages.append(dict(
                        info, type='error',
                        **PGERROR_TO_OE[e.pgcode](self, fg, info, e)))
                    # Failed to write, log to messages, rollback savepoint (to
                    # avoid broken transaction) and keep going
                    cr.execute('ROLLBACK TO SAVEPOINT model_load_save')
                except Exception, e:
                    message = (_('Unknown error during import:') +
                               ' %s: %s' % (type(e), unicode(e)))
                    moreinfo = _('Resolve other errors first')
                    messages.append(dict(info, type='error',
                                         message=message,
                                         moreinfo=moreinfo))
                    # Failed for some reason, perhaps due to invalid data supplied,
                    # rollback savepoint and keep going
                    cr.execute('ROLLBACK TO SAVEPOINT model_load_save')
        if any(message['type'] == 'error' for message in messages):
            cr.execute('ROLLBACK TO SAVEPOINT model_load')
            ids = False
        return {'ids': ids, 'messages': messages}
        
    def unlink(self, cr, uid, ids, context=None):
        data=self.browse(cr,uid,ids)
        for i in data:
            if i.state=='Asignado':
                raise osv.except_osv(
                        ('Error!'),
                        (u'la Asignacion "'+i.descripcion+'" no puede eliminarse'
                         u'\nNo puede eliminar asignaciones con el estatus "Asignado"'))
        retorno=super(jpv_asr_rescurso_general,self).unlink(cr,uid,ids)                 
        return retorno
