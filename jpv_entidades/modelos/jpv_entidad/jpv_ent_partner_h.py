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
#############################################################################

from openerp.osv import fields, osv

class jpv_ent_partner(osv.osv):
    _inherit = 'res.partner'
    
    def limpiar_campos(self,cr,uid,ids,nombre,context=None):
        res={}
        if nombre=='redi':
            res={
            'estado_id':'',
            'municipio_id':'',
            'parroquia_id':'',
            
                }
        if nombre=='estado':
            res={
            'municipio_id':'',
            'parroquia_id':'',
                }
        if nombre=='municipio':
            res={
            'parroquia_id':'',
                }
        return {
         'value':res,
            }

    _columns = {
        'redi_id': fields.many2one('jpv_ent.redis',
                    'REDI',
                    help='Redi de Ubicación'),
        'estado_id': fields.many2one('jpv_ent.estados',
                    'Estado',
                    help='Estado de Ubicación'),
        'municipio_id': fields.many2one('jpv_ent.municipios',
                    'Municipio',
                    help='Municipio de Ubicación'),
        'parroquia_id': fields.many2one('jpv_ent.parroquias',
                    'Parroquia',
                    help='Parroquia de Ubicación'),
        'sector': fields.char('Sector',
                    size=80,
                    help='Sector de Ubicación'
                    ),
        'calle_av': fields.char('Calle/Avenida',
                    size=80,
                    help='Calle/Avenida de Ubicación'
                    ),
        'casa_edif': fields.char('Casa/Edificio',
                    size=80,
                    help='Casa/Edificio de Ubicación'
                    ),
        'piso_apart': fields.char('Piso y Apartemento',
                    size=20,
                    help='Piso y Apartemento de Ubicación'
                    ),
    }
    
class ubicacion_mapa(osv.osv):
    _inherit = "res.partner"

    def open_map(self, cr, uid, ids, context=None):
        address_obj= self.pool.get('res.partner')
        partner = address_obj.browse(cr, uid, ids, context=context)[0]
        url="http://maps.google.com/maps?oi=map&q="
        
        if partner.casa_edif:
            url+='+'+partner.casa_edif.replace(' ','+')
        if partner.calle_av:
            url+='+'+partner.calle_av.replace(' ','+')
        if partner.sector:
            url+='+'+partner.sector.replace(' ','+')
        if partner.parroquia_id:
            url+='+'+partner.parroquia_id.parroquia.replace(' ','+')
        if partner.municipio_id:
            url+='+'+partner.municipio_id.municipio.replace(' ','+')
        if partner.estado_id:
            url+='+'+partner.estado_id.estado.replace(' ','+')
        if partner.country_id:
            url+='+'+partner.country_id.name.replace(' ','+')
        if partner.street:
            url+=partner.street.replace(' ','+')
        if partner.city:
            url+='+'+partner.city.replace(' ','+')
        if partner.state_id:
            url+='+'+partner.state_id.name.replace(' ','+')
        if partner.zip:
            url+='+'+partner.zip.replace(' ','+')
        return {
        'type': 'ir.actions.act_url',
        'url':url,
        'target': 'new'
        }

ubicacion_mapa()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
