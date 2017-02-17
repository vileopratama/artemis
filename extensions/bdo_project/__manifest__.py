# -*- coding: utf-8 -*-
{
    'name': "BDO Project",
    'summary': """
        Manage Project Internal BDO""",
    'description': """
        Management BDO Project
    """,
    'author': "Suhendar",
    'category': 'Project',
    'version': '10.0.1.0.1',
    'depends': ['base','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/bdo_project_menuitem.xml',
        'views/hr_employee_view.xml',
        'views/bdo_project_invoice_view.xml',
        'views/bdo_project_service_view.xml',
        'views/bdo_project_engagement_letter_view.xml',
        'views/res_currency_view.xml',
        'views/bdo_project_target_view.xml',
        'reports/bdo_project_menuitem.xml',
        'reports/bdo_existing_clients_list_report.xml',
        'reports/bdo_project_summary_report.xml',
        'reports/bdo_project_billing_summary_report.xml',
        'reports/bdo_list_of_tax_invoices_report.xml',
        'reports/bdo_schedule_invoices_report.xml',
    ],
    'demo': [
        
    ],
    'website' : "http://www.bdo.co.id",
    'application' : True,
    'installable' : True,
    'auto_install' : False,
}