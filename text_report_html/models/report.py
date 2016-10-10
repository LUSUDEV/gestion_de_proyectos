# -*- coding: utf-8 -*-
##############################################################################
#
#    Venesis, Open Source Management Solution
#    Copyright (C) 2014-Vesesis JPV  (<http://www.juventudproductivavenezonala.com.ve>).
##############################################################################


from openerp import api
from openerp import SUPERUSER_ID
from openerp.osv import osv
from openerp import http
from openerp.addons.web.http import request
from openerp.addons.report.models import report as base_report

import lxml.html
import os
from functools import partial
import logging
import werkzeug.exceptions
import tempfile
from contextlib import closing
import subprocess

_logger = logging.getLogger(__name__) 

class Report(osv.Model):
    _name = "report"
    _inherit="report"
    _description = "text htm Report"
    
    newDescriptonPdf=""
    
    
    @api.v7
    def get_pdf(self, cr, uid, ids, report_name, html=None, data=None, context=None):
        """This method generates and returns pdf version of a report.
        """
        self.newDescriptonPdf="""<div class="row">
                <div class="col-sm-12 col-md-12">
                    <h3 align="center"><img src="jpv2.png" width="150" height="150"  />Log de la Librer&iacute;a Wkhtmltopdf para revisra su proceso y resultado.<img src="jpb.jpg" width="150" height="150" /></h3>
                    <h4>Este m&oacute;dulo una vez instalado genera en esta descripci&oacute;n el dise&ntilde;o, c&oacute;digo y resultado del subproceso del &uacute;ltimo .pdf generado por el sistema con wkhtmltopdf adicionalmente guarda el log informaci&oacute;n extra.</h4>
                    <h4>Se recomienda una vez realizado su revisi&oacute;n Desintalarlo. </h4><hr  style="height:8px;" /><br/><br/>
                    <h3>Resultado: </h3><br/><br/>
                </div>

            </div>"""
        
        if context is None:
            context = {}

        if html is None:
            html = self.get_html(cr, uid, ids, report_name, data=data, context=context)

        html = html.decode('utf-8')  # Ensure the current document is utf-8 encoded.

        # Get the ir.actions.report.xml record we are working on.
        report = self._get_report_from_name(cr, uid, report_name)
        # Check if we have to save the report or if we have to get one from the db.
        save_in_attachment = self._check_attachment_use(cr, uid, ids, report)
        # Get the paperformat associated to the report, otherwise fallback on the company one.
        if not report.paperformat_id:
            user = self.pool['res.users'].browse(cr, uid, uid)
            paperformat = user.company_id.paperformat_id
        else:
            paperformat = report.paperformat_id

        # Preparing the minimal html pages
        css = ''  # Will contain local css
        headerhtml = []
        contenthtml = []
        footerhtml = []
        irconfig_obj = self.pool['ir.config_parameter']
        base_url = irconfig_obj.get_param(cr, SUPERUSER_ID, 'report.url') or irconfig_obj.get_param(cr, SUPERUSER_ID, 'web.base.url')

        # Minimal page renderer
        view_obj = self.pool['ir.ui.view']
        render_minimal = partial(view_obj.render, cr, uid, 'report.minimal_layout', context=context)

        # The received html report must be simplified. We convert it in a xml tree
        # in order to extract headers, bodies and footers.
        try:
            addons_path = http.addons_manifest['text_report_html']['addons_path']
            ruta_donde_guardo_txt=os.path.join(addons_path,'text_report_html','static','description','codigo.txt')
            file_txt = open(ruta_donde_guardo_txt, 'wb+')
            file_txt.write(html)
            file_txt.seek(0)
            msj="Se hizo el text del html que recibe wkhtmltopdf, verlo en la descripción del módulo."
            _logger.info('%s ' ,msj)
            msj="INICIO DEL CÓDIGO."
            _logger.info('%s ' ,msj)
            _logger.info('%s ' ,html)
            msj="FIN DEL CÓDIGO."
            _logger.info('%s ' ,msj)
            root = lxml.html.fromstring(html)
            
            self.newDescriptonPdf+='<hr  style="height:4px;" /><h1>Dise&ntilde;o del html que recibe  wkhtmltopdf </h1>'
            self.newDescriptonPdf+=html
            self.newDescriptonPdf+='''<hr  style="height:4px;" /><h1>C&oacute;digo del html que recibe wkhtmltopdf </h1>
                    <br/><br/>
                    <embed src="/text_report_html/static/description/codigo.txt" width="100%" height="1000px">'''
                    
            match_klass = "//div[contains(concat(' ', normalize-space(@class), ' '), ' {} ')]"

            for node in root.xpath("//html/head/style"):
                css += node.text
                
            for node in root.xpath(match_klass.format('header')):
                body = lxml.html.tostring(node)
                header = render_minimal(dict(css=css, subst=True, body=body, base_url=base_url))
                headerhtml.append(header)

            for node in root.xpath(match_klass.format('footer')):
                body = lxml.html.tostring(node)
                footer = render_minimal(dict(css=css, subst=True, body=body, base_url=base_url))
                footerhtml.append(footer)

            for node in root.xpath(match_klass.format('page')):
                # Previously, we marked some reports to be saved in attachment via their ids, so we
                # must set a relation between report ids and report's content. We use the QWeb
                # branding in order to do so: searching after a node having a data-oe-model
                # attribute with the value of the current report model and read its oe-id attribute
                if ids and len(ids) == 1:
                    reportid = ids[0]
                else:
                    oemodelnode = node.find(".//*[@data-oe-model='%s']" % report.model)
                    if oemodelnode is not None:
                        reportid = oemodelnode.get('data-oe-id')
                        if reportid:
                            reportid = int(reportid)
                    else:
                        reportid = False

                # Extract the body
                body = lxml.html.tostring(node)
                reportcontent = render_minimal(dict(css=css, subst=False, body=body, base_url=base_url))

                contenthtml.append(tuple([reportid, reportcontent]))

        except lxml.etree.XMLSyntaxError as e:
            msj="Hubo una except cuando intento crear el PDF."
            _logger.warning('%s ' ,msj)
            _logger.warning('%s ' , e)
            contenthtml = []
            contenthtml.append(html)
            save_in_attachment = {}  # Don't save this potentially malformed document

        # Get paperformat arguments set in the root html tag. They are prioritized over
        # paperformat-record arguments.
        specific_paperformat_args = {}
        for attribute in root.items():
            if attribute[0].startswith('data-report-'):
                specific_paperformat_args[attribute[0]] = attribute[1]

        # Run wkhtmltopdf process
        msj="""PARAMETROS QUE SE LE PASAN AL METODO _run_wkhtmltopdf(self, cr, uid, headers, footers, bodies, landscape, paperformat, spec_paperformat_args=None, save_in_attachment=None):
        *******Inicio del Código de la headerhtml***************
         %s 
        **********Fin del código headerhtml**********************
        ***********Inicio del código del footerhtml**************
         %s
        ************Fin del código del footerhtml*************
        variable  uid = %d
        variable context.get('landscape')= %s
        variable paperformat=%s
        variable specific_paperformat_args= %s
        variable save_in_attachment = %s
        """ % (
            headerhtml,
            footerhtml,
            uid,
            context.get('landscape'),paperformat,
            specific_paperformat_args,
            save_in_attachment
            )
        _logger.info('%s ' ,msj)
        headeroot = lxml.html.fromstring(headerhtml[0])
        headerbase=" No Tiene..."
        for headerootnode in headeroot.xpath("//base"):
            headerbase=headerootnode.base
        bodyroot = lxml.html.fromstring(contenthtml[0][1])
        bodybase=" No Tiene..."
        for bodyrootnode in bodyroot.xpath("//base"):
            bodybase=bodyrootnode.base
        footeroot = lxml.html.fromstring(footerhtml[0])
        footerbase=" No Tiene..."
        for footerootnode in bodyroot.xpath("//base"):
            footerbase=footerootnode.base
        self.newDescriptonPdf+="""<hr  style="height:4px;" /><h1>Base de peticiones:</h1></h1>
                <h3>header= %s <br/>
                body= %s <br/>
                footer= %s 
                </h3> <hr  style="height:4px;" />""" % (headerbase,bodybase,footerbase)
        return self._run_wkhtmltopdf(
            cr, uid, headerhtml, footerhtml, contenthtml, context.get('landscape'),
            paperformat, specific_paperformat_args, save_in_attachment
        )
        
    def _run_wkhtmltopdf(self, cr, uid, headers, footers, bodies, landscape, paperformat, spec_paperformat_args=None, save_in_attachment=None):
        """Execute wkhtmltopdf as a subprocess in order to convert html given in input into a pdf
        document.

        :param header: list of string containing the headers
        :param footer: list of string containing the footers
        :param bodies: list of string containing the reports
        :param landscape: boolean to force the pdf to be rendered under a landscape format
        :param paperformat: ir.actions.report.paperformat to generate the wkhtmltopf arguments
        :param specific_paperformat_args: dict of prioritized paperformat arguments
        :param save_in_attachment: dict of reports to save/load in/from the db
        :returns: Content of the pdf as a string
        """
        command_args = []

        # Passing the cookie to wkhtmltopdf in order to resolve internal links.
        try:
            if request:
                command_args.extend(['--cookie', 'session_id', request.session.sid])
        except AttributeError as e:
            msj="Al pasar la cookie para wkhtmltopdf con el fin de resolver los enlaces internos."
            msj=msj+' '+e
            _logger.warning(' %s ' ,msj)
            pass
        msj=""" variable command_args luego que se le agrega --cookies y sesion_id.
        %s
        """ % command_args
        _logger.info('%s ' ,msj)
        #~ self.newDescriptonPdf+=msj
        # Wkhtmltopdf arguments
        #~ command_args.extend(['--quiet'])  # Less verbose error messages
        if paperformat:
            # Convert the paperformat record into arguments
            command_args.extend(self._build_wkhtmltopdf_args(paperformat, spec_paperformat_args))
        # Force the landscape orientation if necessary
        if landscape and '--orientation' in command_args:
            command_args_copy = list(command_args)
            for index, elem in enumerate(command_args_copy):
                if elem == '--orientation':
                    del command_args[index]
                    del command_args[index]
                    command_args.extend(['--orientation', 'landscape'])
        elif landscape and not '--orientation' in command_args:
            command_args.extend(['--orientation', 'landscape'])
        msj=""" variable command_args luego que se confirma la orientación.
          %s
        """ % command_args
        #~ self.newDescriptonPdf+=msj
        # Execute WKhtmltopdf
        pdfdocuments = []
        temporary_files = []

        for index, reporthtml in enumerate(bodies):
            local_command_args = []
            pdfreport_fd, pdfreport_path = tempfile.mkstemp(suffix='.pdf', prefix='report.tmp.')
            msj=""" pdf report pdfreport_fd y pdfreport_path.
            pdfreport_fd = %d 
            pdfreport_path = %s
            """ % (pdfreport_fd,pdfreport_path)
            _logger.info('%s ' ,msj)
            #~ self.newDescriptonPdf+=msj
            temporary_files.append(pdfreport_path)
            # Directly load the document if we already have it
            if save_in_attachment and save_in_attachment['loaded_documents'].get(reporthtml[0]):
                with closing(os.fdopen(pdfreport_fd, 'w')) as pdfreport:
                    pdfreport.write(save_in_attachment['loaded_documents'][reporthtml[0]])
                pdfdocuments.append(pdfreport_path)
                continue
            else:
                os.close(pdfreport_fd)

            # Wkhtmltopdf handles header/footer as separate pages. Create them if necessary.
            if headers:
                head_file_fd, head_file_path = tempfile.mkstemp(suffix='.html', prefix='report.header.tmp.')
                msj=""" html  temporal report.header.tmp report ruta y id.
                head_file_fd = %d 
                pdfreport_path = %s
                """ % (head_file_fd,head_file_path)
                _logger.info('%s ' ,msj)
                #~ self.newDescriptonPdf+=msj
                temporary_files.append(head_file_path)
                with closing(os.fdopen(head_file_fd, 'w')) as head_file:
                    head_file.write(headers[index])
                local_command_args.extend(['--header-html', head_file_path])
                msj="""
                local_command_args cuando se le adiciona el --header-html
                %s 
                """ % local_command_args
                _logger.info('%s ' ,msj)
                #~ self.newDescriptonPdf+=msj
            if footers:
                foot_file_fd, foot_file_path = tempfile.mkstemp(suffix='.html', prefix='report.footer.tmp.')
                temporary_files.append(foot_file_path)
                msj=""" html  temporal report.footer.tmp report ruta y id.
                foot_file_fd = %d 
                foot_file_path = %s
                """ % (foot_file_fd,foot_file_path)
                _logger.info('%s ' ,msj)
                #~ self.newDescriptonPdf+=msj
                with closing(os.fdopen(foot_file_fd, 'w')) as foot_file:
                    foot_file.write(footers[index])
                local_command_args.extend(['--footer-html', foot_file_path])
                msj="""
                local_command_args cuando se le adiciona el --footer-html
                %s 
                """ % local_command_args
                _logger.info('%s ' ,msj)
                #~ self.newDescriptonPdf+=msj
            # Body stuff
            content_file_fd, content_file_path = tempfile.mkstemp(suffix='.html', prefix='report.body.tmp.')
            msj=""" content  temporal report.body.tmp report ruta y id.
                content_file_fd = %d 
                content_file_path = %s
                """ % (content_file_fd,content_file_path)
            _logger.info('%s ' ,msj)
            #~ self.newDescriptonPdf+=msj
            temporary_files.append(content_file_path)
            with closing(os.fdopen(content_file_fd, 'w')) as content_file:
                content_file.write(reporthtml[1])

            try:
                msj=""" Obtener ruta del binario de la libreria Wkhtmltopdf .
                %s
                """ % base_report._get_wkhtmltopdf_bin()
                _logger.info('%s ' ,msj)
                #~ self.newDescriptonPdf+=msj
                wkhtmltopdf = [base_report._get_wkhtmltopdf_bin()] + command_args + local_command_args
                wkhtmltopdf += [content_file_path] + [pdfreport_path]
                process = subprocess.Popen(wkhtmltopdf, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                msj=""" Resultado del subproceso para ejecutar el PDF con wkhtmltopdf .
                 %s
                 %s
                """ % (out,err)
                _logger.info('%s ' ,msj)
                self.newDescriptonPdf+='<br/><br/><h1>Resultado del subproceso que jecutar wkhtmltopdf para generar el pdf. '
                self.newDescriptonPdf+= '<br/><p>'+out+'<br/>'+err+'<br/></p></h1><hr  style="height:4px;" />'
                addons_path = http.addons_manifest['text_report_html']['addons_path']
                ruta_donde_guardo_html=os.path.join(addons_path,'text_report_html','static','description','index.html')
                file_html = open(ruta_donde_guardo_html, 'wb+')
                file_html.write(self.newDescriptonPdf)
                file_html.seek(0)
                if process.returncode not in [0, 1]:
                    raise osv.except_osv(_('Report (PDF)'),
                                         _('Wkhtmltopdf failed (error code: %s). '
                                           'Message: %s') % (str(process.returncode), err))

                # Save the pdf in attachment if marked
                if reporthtml[0] is not False and save_in_attachment.get(reporthtml[0]):
                    with open(pdfreport_path, 'rb') as pdfreport:
                        attachment = {
                            'name': save_in_attachment.get(reporthtml[0]),
                            'datas': base64.encodestring(pdfreport.read()),
                            'datas_fname': save_in_attachment.get(reporthtml[0]),
                            'res_model': save_in_attachment.get('model'),
                            'res_id': reporthtml[0],
                        }
                        try:
                            self.pool['ir.attachment'].create(cr, uid, attachment)
                        except AccessError:
                            _logger.warning("Cannot save PDF report %r as attachment",
                                            attachment['name'])
                        else:
                            _logger.info('The PDF document %s is now saved in the database',
                                         attachment['name'])

                pdfdocuments.append(pdfreport_path)
            except:
                raise

        # Return the entire document
        if len(pdfdocuments) == 1:
            entire_report_path = pdfdocuments[0]
        else:
            entire_report_path = self._merge_pdf(pdfdocuments)
            temporary_files.append(entire_report_path)

        with open(entire_report_path, 'rb') as pdfdocument:
            content = pdfdocument.read()

        # Manual cleanup of the temporary files
        for temporary_file in temporary_files:
            try:
                os.unlink(temporary_file)
            except (OSError, IOError):
                _logger.error('Error when trying to remove file %s' % temporary_file)
        return content
