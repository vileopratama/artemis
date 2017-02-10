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
    'depends': ['base','hr','crm'],
    'data': [
        'views/hr_employee.xml',
        'views/bdo_project_invoice.xml',
        'views/bdo_project_service.xml',
        'views/bdo_project.xml',
    ],
    'demo': [
        #'demo/demo.xml',
    ],
    'application' : True,
    'installable' : True,
    'auto_install' : False,
}