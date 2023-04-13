from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    product_tracking = fields.Selection(related='product_id.tracking')

    def action_open_eq(self):
        """
        :return: Open related record or Create new record
        """
        eq = self.env['maintenance.equipment'].search([('lot_id', '=', self.id)])

        action = self.env.ref('maintenance.hr_equipment_action').read([])[0]
        action['view_mode'] = 'form'
        action['views'] = [(False, 'form')]
        action['target'] = 'new'
        if eq:
            action['res_id'] = eq.id
            action['context'] = {'create': False}
        else:
            action['context'] = {
                'default_name': self.product_id.name,
                'default_serial_no': self.ref or self.name,
                'default_note': self.note,
                'default_effective_date': self.create_date,
                'default_location': self.quant_ids.filtered(lambda q: q.location_id.usage == 'internal' and q.quantity > 0).location_id.display_name or '',
                'default_lot_id': self.id,
                'create': False
            }
        return action
