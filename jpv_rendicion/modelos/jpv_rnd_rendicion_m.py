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
#    Modulo Desarrollado por Juventud Productiva (Jose Mancilla)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
#############################################################################

import openerp
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _
from openerp.http import request
import time
from datetime import datetime,date
from openerp.addons.jpv_rendicion.controladores import comunes
from openerp import SUPERUSER_ID

class jpv_rnd_rendicion(osv.osv):
    _name='jpv_rnd.rendicion'
    _rec_name="proyecto_id"
   
    def get_data_field(self, cr, uid, ids, nombre_campo, arg, context):
        res={}
        campo_id=self.pool.get('ir.model.fields').search(cr, uid, [('name','=',nombre_campo),('model','=',self._name)])
        pregunta_id=self.pool.get('jpv_conf.preguntas').search(cr, uid, [('field_muestra_ids','=',campo_id[0])])
        input_line_obj=self.pool.get('jpv_rnd.input_line')
        records=self.browse(cr, uid, ids)
        for r in records:
            respuesta_id=input_line_obj.search(cr , uid ,
                                    [('pregunta_id','in',pregunta_id),
                                    ('rendicion_id','=', r.id)],order='create_date DESC',limit=1)
            respuesta_data=input_line_obj.browse(cr,uid,respuesta_id)
            if respuesta_data:
                res[r.id]=respuesta_data.respuesta;
            else:
                if nombre_campo == 'estatus':
                    res[r.id]='Sin iniciar'
                else:
                    res[r.id]=False
            if nombre_campo == 'estatus':
                if r.estatus_proyecto != res[r.id]:
                    write_status=self.write(cr, SUPERUSER_ID, r.id, {'estatus_proyecto':res[r.id]})
            if nombre_campo == 'monto_gastado':
                if r.avance_financiero != res[r.id] and res[r.id] != False:
                    write_financ=self.write(cr, SUPERUSER_ID, r.id, {'avance_financiero':res[r.id]})
            if nombre_campo == 'avance_fisico':
                if r.avance_fisico_porc != res[r.id] and res[r.id] != False:
                    write_avance=self.write(cr, SUPERUSER_ID, r.id, {'avance_fisico_porc':res[r.id]})
        return res;
    
    def generar_notificaciones(self, cr, uid, ids=None, context=None):
        self.pool.get('jpv_rnd.notificaciones_rendicion').consulta_rendiciones(cr,uid)
        return True
        
    def instanciar_objetos(self, cr, uid, objeto_name,objeto_id=None, domain=None, orden=None, limite=None):
        obj=self.pool.get(objeto_name)
        if objeto_id == None:
            if domain:
                obj_id=obj.search(cr,uid,domain,order=orden,limit=limite)
            else:
                return False
        else:
            obj_id=objeto_id
        obj_data=obj.browse(cr,uid,obj_id)
        return obj_data    
        
    def tiempo_validez_notificacion_get(self, cr, uid, proyecto_id):
        redicion_data=self.instanciar_objetos(cr, uid, 'jpv_rnd.rendicion', None,[('proyecto_id','=',proyecto_id)])
        if not len(redicion_data):
            return 'sin_rendicion'
        avance_data=self.instanciar_objetos(cr, uid, 'jpv_rnd.avance', None,[('rendicion_id','=',redicion_data.id)],'create_date DESC',1)
        if not avance_data.create_date:
            return 'sin_rendicion'
        tiempo_data=self.instanciar_objetos(cr, uid, 'jpv_rnd.tiempo_validez', None,[('model_id','=',redicion_data._name)])
        hoy=datetime.today()
        fecha_avance=datetime.strptime(avance_data.create_date,'%Y-%m-%d %H:%M:%S')
        diferencia=hoy-fecha_avance
        diferencia=diferencia.days
        if diferencia > tiempo_data.dias_validez:
            retorno='vencidas'
        elif diferencia <= tiempo_data.dias_validez and diferencia > tiempo_data.dias_validez*0.80 :
            retorno='por_vencer'
        elif diferencia < tiempo_data.dias_validez*0.80:
            retorno='vigentes'
        return retorno
        
    _columns = {
        'entidad_id':fields.related('proyecto_id',
                    'partner_id', string='Entidad', 
                    type='many2one', relation='res.partner',
                    help="""Entidad a la cual esta asociada el proyecto""",
                    readonly=True),
       
        'monto':fields.related('proyecto_id',
                    'monto_proyecto', string='Monto del Proyecto', 
                    type='float',
                    help="""Monto total del proyecto""",
                    ),
                    
        'proyecto_id':fields.many2one(
                    'jpv_cp.carga_proyecto',
                    'Proyecto',help="Proyecto",
                    readonly=True),
        
        'rendicion_line':fields.one2many(
                    'jpv_rnd.avance',
                    'rendicion_id',
                    'Avances'),
                    
        'tipo_ejecucion':fields.function(get_data_field, type='char', string="Tipo de Ejecución"),
        
        
        'inicio_administrativo':fields.function(get_data_field, type='char', string="Inició Administrativamente"),
        
        
        'adjudicacion':fields.function(get_data_field, type='char', string="Adjudicación de Contrato"),
        
        
        'nro_contrato':fields.function(get_data_field, type='char', string="Número de Contrato"),
        
        
        'rif_empresa':fields.function(get_data_field, type='char', string="Rif de la Empresa contratada"),
        
        
        'nombre_institucion':fields.function(get_data_field, type='char', string="Nombre de la institución Encargada"),
        
        
        'rif_institucion':fields.function(get_data_field, type='char', string="Rif de la Institución Encargada"),
        
        
        'fecha_inicio_proyecto':fields.function(get_data_field, type='char', string="Fecha de Inicio del Proyecto"),
            
        
        
        'estatus':fields.function(get_data_field, type='char', string="Estatus del Proyecto"),
        
        
        'estatus_proyecto':fields.char("Estatus del Proyecto"),
        
        
        'state':fields.selection([('ejecucion','En Ejecucion'),
                                    ('culminada','Culminada')],
                                            string="Estatus de la rendicion", 
                                            help="Este es el estatus de la rendición"),
        
        
        'monto_gastado':fields.function(get_data_field, type='char', string="Monto Pagado"),
        
        'avance_financiero':fields.char("Avance Financiero"),
        
        
        'movimiento_ids':fields.many2many('jpv.movimientos_cuentas',
                                          'jpv_rnd_rendicion_movimiento',
                                          'rendicion_id', 
                                          'movimiento_id',
                                          'Movimientos'),
        
        
        'avance_fisico':fields.function(get_data_field, type='char', string="Avance Fisico" ),
        
        'avance_fisico_porc':fields.char("Avance Físico"),
        
        
        'adquisicion_equipos':fields.one2many('jpv_cp.equipos','rendicion_id',
                                            string="Adquisicion de Equipos", 
                                            help="Aqui se agregan los equipos a adquirir"),
                                            
        'adquisicion_vehiculo':fields.one2many('jpv_cp.vehiculo','rendicion_id',
                                            string="Adquisicion de Vehiculos", 
                                            help="Aqui se agregan los Vehiculos a adquirir"),
                                            
        'adquisicion_materiales_consumo':fields.one2many('jpv_cp.materiales_consumo','rendicion_id',
                                            string="Adquisicion de Materiales de Consumo", 
                                            help="Aqui se agregan los materiales de consumo a adquirir"),
                                            
        'adquisicion_maquinaria':fields.one2many('jpv_cp.maquinaria','rendicion_id',
                                            string="Adquisicion de Maquinaria", 
                                            help="Aqui se agregan la Maquinaria a adquirir"),
                                            
                                            
        'adquisicion_semovientes':fields.one2many('jpv_cp.semovientes_caracteristicas','rendicion_id',
                                            string="Adquisicion de Semovientes", 
                                            help="Aqui se agregan el Semoviente a adquirir"),
        
        'obra_civil':fields.boolean('Obra Civil'),
        
        'tipo_obra':fields.selection([('construccion','Construcción'),
                                    ('ampliacion','Ampliación'),
                                    ('rehabilitacion','Rehabilitacion')],
                                            string="Tipo de obra", 
                                            help="Aqui se agrega el Tipo de obra"),
        
        'cantidad_estimada_obra':fields.float('Cantidad Estimada de la Obra',
                                            help="Aqui se agrega el Tipo de obra"),
        
        'unidad_medicion_obra':fields.many2one('jpv_cp.unidades_obra_civil_config',
                                                'Unidad', 
                                                required=False, 
                                                help=''),
                                            
            
    }
    
    
    _defaults={
        'state':'ejecucion',
    }
    
    _order = 'create_date desc, id desc'

    def revertir_culminacion(self, cr, uid, ids, context):
        rendicion_data=self.browse(cr,uid,ids)
        if rendicion_data.state == 'culminada':
            self.write(cr,uid,ids,{'state':'ejecucion'})
            rendicion_data=self.browse(cr,uid,ids)
            disp_mantenimiento_entidad=self.pool.get('jpv_ent.entidades').search_read(
                                                                            cr,
                                                                            uid,
                                                                            [('parent_id',
                                                                                '=',rendicion_data.entidad_id.id)],
                                                                            ['monto_disp_mantenimiento'])
            lista_movimientos=[]
            movimientos_lista=list(rendicion_data.movimiento_ids)
            if len(movimientos_lista):
                movimientos_lista.sort(comunes.compara_movimientos)
                for movimiento in movimientos_lista:
                    lista_movimientos.append(movimiento.id)
                    monto_egreso=movimiento.monto_ingreso
                obj_movimiento=self.pool.get('jpv.movimientos_cuentas')
                cuenta_id=rendicion_data.proyecto_id.cuenta_id.id
                reverso_culminacion=obj_movimiento.movimiento_egreso(cr,SUPERUSER_ID,cuenta_id,
                                                                    monto_egreso,'Reverso Culminación',
                                                                    rendicion_data.proyecto_id.correlativo,
                                                                    'jpv_cp.carga_proyecto',rendicion_data.proyecto_id.id,
                                                                    rendicion_data.proyecto_id.periodo_id.id,
                                                                    rendicion_data.entidad_id.id,
                                                                    )
                lista_movimientos.append(reverso_culminacion['movimiento_id_egreso'])
                write_mov_ids=self.write(cr,uid,rendicion_data.id,{'movimiento_ids':[6,False,[lista_movimientos]]})
            self.pool.get('jpv_cp.carga_proyecto').write(cr,SUPERUSER_ID,
                                            rendicion_data.proyecto_id.id,
                                            {'state':'aprobado'},0)
        return True

    def unlink(self,cr,uid,ids,context=None):
        rendicion_data=self.browse(cr,uid,ids)
        unlink_id={}
        for rendicion in rendicion_data:
            if rendicion.state=='culminada':
                raise osv.except_osv(
                    ('Error!'),
                    (u'El Proyecto "%s" ya esta Culminado.\n'\
                    ' No puede eliminar rendiciones de proyectos culminados' % (rendicion.proyecto_id.correlativo)))
            else:
                unlink_id=super(jpv_rnd_rendicion,self).unlink(cr,uid,ids,context)
        return unlink_id 

        
        
class jpv_cp_equipos_inherit(osv.osv):
    _inherit="jpv_cp.equipos"
   
        
        
    _columns = {

        'rendicion_id':fields.many2one(
                    'jpv_rnd.rendicion',
                    'Rendicion',help="Rendicion"
                    ),
        
            
    }
    
    
    
class jpv_cp_vehiculo_inherit(osv.osv):
    _inherit="jpv_cp.vehiculo"
   
        
        
    _columns = {

        'rendicion_id':fields.many2one(
                    'jpv_rnd.rendicion',
                    'Rendicion',help="Rendicion"
                    ),
        
            
    }



class jpv_cp_materiales_consumo_inherit(osv.osv):
    _inherit="jpv_cp.materiales_consumo"
   
        
        
    _columns = {

        'rendicion_id':fields.many2one(
                    'jpv_rnd.rendicion',
                    'Rendicion',help="Rendicion"
                    ),
        
            
    }


class jpv_cp_maquinaria_inherit(osv.osv):
    _inherit="jpv_cp.maquinaria"
   
        
        
    _columns = {

        'rendicion_id':fields.many2one(
                    'jpv_rnd.rendicion',
                    'Rendicion',help="Rendicion"
                    ),
        
            
    }
    
    
class jpv_cp_semovientes_inherit(osv.osv):
    _inherit="jpv_cp.semovientes_caracteristicas"
   
        
        
    _columns = {

        'rendicion_id':fields.many2one(
                    'jpv_rnd.rendicion',
                    'Rendicion',help="Rendicion"
                    ),
        
            
    }

