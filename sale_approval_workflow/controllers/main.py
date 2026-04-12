from odoo import http
from odoo.http import request

class CustomerAPI(http.Controller):

    @http.route('/api/customers', type='json', auth='user', methods=['POST'])
    def get_customers(self):
        customers = request.env['res.partner'].search([])

        return [{
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone
        } for c in customers]