# -*- coding: utf-8 -*-
{
    'name': "CRM Proposal",
    'summary': """
        Manage CRM Proposal BDO""",
    'description': """
        Management BDO Proposal CRM
    """,
    'author': "Suhendar",
    'category': 'BDO CRM',
    'version': '10.0.1.0.1',
    'depends': [
        'crm',
    ],
    'data': [
        'views/res_config_view.xml',
        'views/crm_proposal_view.xml'
    ],
    'website': "http://www.bdo.co.id",
    'application': False,
    'installable': True,
    'auto_install': False,
}
