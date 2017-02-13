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
        'views/bdo_project_menuitem.xml',
        'views/hr_employee.xml',
        'views/bdo_project_invoice.xml',
        'views/bdo_project_service.xml',
        'views/bdo_project_engagement letter.xml',
        'views/res_currency.xml',
        'views/bdo_project_target.xml',
    ],
    'demo': [
        
    ],
    'website' : "http://www.bdo.co.id",
    'application' : True,
    'installable' : True,
    'auto_install' : False,
}