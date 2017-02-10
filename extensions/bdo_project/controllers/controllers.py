# -*- coding: utf-8 -*-
from odoo import http

# class BdoProject(http.Controller):
#     @http.route('/bdo_project/bdo_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bdo_project/bdo_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bdo_project.listing', {
#             'root': '/bdo_project/bdo_project',
#             'objects': http.request.env['bdo_project.bdo_project'].search([]),
#         })

#     @http.route('/bdo_project/bdo_project/objects/<model("bdo_project.bdo_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bdo_project.object', {
#             'object': obj
#         })