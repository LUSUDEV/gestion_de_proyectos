# -*- encoding: utf-8 -*-
from openerp.osv import osv, fields
from openerp.report import report_sxw

class reporte_csv_wizard(osv.TransientModel):
    _name='jpv_asr.asignacion_recurso_wizard'
    
    
    
    _columns={

        'tipo_cuenta':fields.many2one('jpv.tipo_cuentas','Tipo de Cuenta', help="Seleccione el tipo de cuenta a la cual desea asignar"),
                
        'res_partner_ids':fields.many2many(
                    'res.partner',
                    'res_partner_wizard_rel',
                    'wizard_id',
                    'res_partner_id',
                    'Entidad o Institucion',
                    help="Organizaciones que se van a incluir en la lista a exportar"
                    ),
    }
    
    def onchange_tipo_cuenta(self,cr,uid,ids,tipo_cuenta,context=None):
        partner_ids=[]
        cuentas_obj=self.pool.get('jpv.cuentas')
        cuentas_ids=cuentas_obj.search(cr,uid,[('tipo_cuenta_id','=',tipo_cuenta)])
        cuentas_data=cuentas_obj.browse(cr,uid,cuentas_ids,context)
        for r in cuentas_data:
            partner_ids.append(r.partner_id.id)
        partner_ids=list(set(partner_ids))
        domain = {'res_partner_ids':[('id', 'in', partner_ids)]}
        return {'domain': domain}
    
