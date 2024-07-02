# -*- coding: utf-8 -*-
# from odoo import http


# class Salutation(http.Controller):
#     @http.route('/salutation/salutation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/salutation/salutation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('salutation.listing', {
#             'root': '/salutation/salutation',
#             'objects': http.request.env['salutation.salutation'].search([]),
#         })

#     @http.route('/salutation/salutation/objects/<model("salutation.salutation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('salutation.object', {
#             'object': obj
#         })

