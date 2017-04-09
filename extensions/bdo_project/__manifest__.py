# -*- coding: utf-8 -*-
{
    'name': "BDO Project",
    'summary': """
        Manage CRM Project Internal BDO""",
    'description': """
        Management BDO Project
    """,
    'author': "Suhendar",
    'category': 'BDO CRM',
    'version': '10.0.1.0.1',
    'depends': [
        'base','web_highcharts_pie','hr','crm_proposal','crm_prospective_client',
    ],
    'data': [
        'data/ir_ui_view.xml',
        'security/bdo_project_security.xml',
        'security/ir.model.access.csv',
        'views/bdo_project_menuitem.xml',
        'views/web_templates.xml',
        'views/res_users_view.xml',
        'views/hr_employee_view.xml',
        'views/bdo_project_service_view.xml',
        'views/bdo_project_view.xml',
        'views/bdo_project_lines_view.xml',
        'views/res_currency_view.xml',
        'wizard/bdo_project_target_to_invoice.xml',
        'wizard/bdo_project_invoice_to_paid.xml',
        'views/bdo_project_target_view.xml',
        'views/bdo_project_invoice_view.xml',
        'views/res_partner_view.xml',
        'reports/bdo_project_summary_report.xml',
        'reports/bdo_project_billing_summary_report.xml',

    ],
	"qweb": [
        'static/src/xml/bdo_project.xml',
    ],
    'website' : "http://www.bdo.co.id",
    'application' : True,
    'installable' : True,
    'auto_install' : False,
}