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
        'base',
        'hr'
    ],
    'data': [
        'security/bdo_project_security.xml',
        'security/ir.model.access.csv',
        'views/bdo_project_menuitem.xml',
        'views/res_users.xml',
        'views/hr_employee_view.xml',
        'views/bdo_project_service_view.xml',
        'views/bdo_project_view.xml',
        'views/bdo_project_lines_view.xml',
        'views/res_currency_view.xml',
        'wizard/bdo_project_target_to_invoice.xml',
        'wizard/bdo_project_invoice_to_paid.xml',
        'views/bdo_project_target_view.xml',
        'views/bdo_project_invoice_view.xml',
        'data/hr_employee.xml',
        'data/bdo_project_service.xml',
        #'reports/bdo_project_menuitem.xml',
        #'reports/bdo_existing_clients_list_report.xml',
        ##'reports/bdo_project_summary_report.xml',
        #'reports/bdo_project_billing_summary_report.xml',
        #'reports/bdo_list_of_tax_invoices_report.xml',
        #'reports/bdo_schedule_invoices_report.xml',
    ],
    'website' : "http://www.bdo.co.id",
    'application' : True,
    'installable' : True,
    'auto_install' : False,
}