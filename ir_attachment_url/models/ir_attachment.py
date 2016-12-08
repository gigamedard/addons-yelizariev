# -*- coding: utf-8 -*-
import re
import requests
import base64
from odoo import api, models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.depends('store_fname', 'db_datas')
    def _compute_datas(self):
        bin_size = self._context.get('bin_size')
        url_records = self.filtered(lambda r: r.type == 'url' and r.url)
        for attach in url_records:
            if not bin_size:
                r = requests.get(attach.url)
                attach.datas = base64.b64encode(r.content)
            else:
                attach.datas = "1.00 Kb"

        super(IrAttachment, self - url_records)._compute_datas()

    @api.multi
    def write(self, vals):
        self.check('write', values=vals)
        url = vals.get('url')
        url_assets_records = self.filtered(lambda r: r.type == 'url' and r.res_model == 'ir.ui.view')
        super(IrAttachment, self - url_assets_records).write(vals)
        if url and re.match(r'^/web/content/.*', url):
            vals.pop('url', False)
        super(IrAttachment, url_assets_records).write(vals)
        return True