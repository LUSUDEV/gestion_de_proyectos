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

from openerp.osv import osv
import time
from openerp.report import report_sxw

class reporte_saldo_movimiento(report_sxw.rml_parse):
    def __init__(self , cr, uid, name, context):
        super(reporte_saldo_movimiento,self).__init__(cr,uid,name,context)
        self.localcontext.update({
            'time':time,
        })
        self.context = context

class report_datos_personales(osv.AbstractModel):
    _name = "report.ept_cuentas.id_cta_saldo_ird_report_qweb"
    _inherit = "report.abstract_report"
    _template = "ept_cuentas.id_cta_saldo_ird_report_qweb"
    _wrapped_report_class = reporte_saldo_movimiento
# report_sxw.report_sxw('ept_cuentas.ept_cuenta_saldo_ird_t', 'ept.cuentas', 'local_pi/ept_cuentas/reportes/ept_cuenta_saldo_ird_t.rml', parser=reporte_saldo_movimiento,header=False)
