# -*- encoding: utf-8 -*-

from openerp.osv import osv
import time
from openerp import http
from openerp.report import report_sxw
from openerp import SUPERUSER_ID

class jpv_rnd_reporte_ejecucion(report_sxw.rml_parse):
    def __init__(self , cr, uid, name, context):
        super(jpv_rnd_reporte_ejecucion,self).__init__(cr,uid,name,context)
        self.localcontext.update({
            'time':time,
            'get_data': self.get_data,
        })
        self.context = context
    
    def get_data(self, rendicion_id):
        cr, uid, context = http.request.cr, http.request.uid, http.request.context
        list_files=[]
        print rendicion_id
        input_line_obj=self.pool.get('jpv_rnd.input_line')
        input_line_ids=input_line_obj.search(cr,SUPERUSER_ID,[('rendicion_id','=',rendicion_id),
                                                    ('tipo_pregunta','=','img')])
        input_line_data=input_line_obj.browse(cr,SUPERUSER_ID,input_line_ids)
        print input_line_data
        print input_line_data
        print input_line_data
        for input_line in input_line_data:
            for files in input_line.files:
                list_files.append(files)
        return list_files

        
class report_reporte_ejecucion(osv.AbstractModel):
    _name = "report.jpv_rendicion.id_template_reporte_ejecucion_qweb"
    _inherit = "report.abstract_report"
    _template = "jpv_rendicion.id_template_reporte_ejecucion_qweb"
    _wrapped_report_class = jpv_rnd_reporte_ejecucion
# report_sxw.report_sxw('report.report_reporte_ejecucion', 'jpv_rnd.rendicion', 'local_addons_ep1561/jpv_rendicion/reportes/report_reporte_ejecucion_jpv.rml', parser=jpv_rnd_reporte_ejecucion,header=False)

class report_reporte_ejecucion_website(osv.AbstractModel):
    _name = "report.jpv_rendicion.id_template_reporte_ejecucion_qweb_website"
    _inherit = "report.abstract_report"
    _template = "jpv_rendicion.id_template_reporte_ejecucion_qweb_website"
    _wrapped_report_class = jpv_rnd_reporte_ejecucion
# report_sxw.report_sxw('report.report_reporte_ejecucion_website', 'jpv_rnd.rendicion', 'local_addons_ep1561/jpv_rendicion/reportes/report_reporte_ejecucion_jpv.rml', parser=jpv_rnd_reporte_ejecucion,header=False)
