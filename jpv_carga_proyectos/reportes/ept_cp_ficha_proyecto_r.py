# -*- encoding: utf-8 -*-

from openerp.osv import osv
import time
from openerp.report import report_sxw

class ept_cp_ficha_proyecto(report_sxw.rml_parse):
    def __init__(self , cr, uid, name, context):
        super(ept_cp_ficha_proyecto,self).__init__(cr,uid,name,context)
        self.localcontext.update({
            'time':time,
            'get_data': self.get_data,
        })
        self.context = context
    
    def get_data(self):
        return 'hola mundo'

        
class report_ficha_proyecto_ept(osv.AbstractModel):
    _name = "report.ept_carga_proyectos.ficha_proyecto_qweb"
    _inherit = "report.abstract_report"
    _template = "ept_carga_proyectos.ficha_proyecto_qweb"
    _wrapped_report_class = ept_cp_ficha_proyecto
# report_sxw.report_sxw('report.report_ficha_proyecto_ept', 'ept_cp.carga_proyecto', 'local_addons_ep1561/ept_carga_proyectos/report/report_ficha_proyecto_ept.rml', parser=ept_cp_ficha_proyecto,header=False)
