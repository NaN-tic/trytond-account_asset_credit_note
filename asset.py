# This file is part of Tryton.  The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.
from decimal import Decimal
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Bool, If
from trytond.transaction import Transaction

__all__ = ['Asset', 'UpdateAssetStart', 'UpdateAsset']


class Asset(metaclass=PoolMeta):
    __name__ = 'account.asset'

    supplier_refund_invoice_line = fields.Many2One('account.invoice.line',
        'Supplier Refund Invoice Line',
        domain=[
            If(Eval('product', None) == None,
                ('product', '=', -1),
                ('product', '=', Eval('product', -1)),
                ),
            ('invoice.type', '=', 'in'),
            ['OR',
                ('quantity', '<', 0),
                ('unit_price', '<', 0),
                ],
            ['OR',
                ('company', '=', Eval('company', -1)),
                ('invoice.company', '=', Eval('company', -1)),
                ],
            ],
        states={
            'readonly': (Eval('lines', [0]) | (Eval('state') != 'draft')),
            'invisible': ~Bool(Eval('supplier_refund_invoice_line', 1)),
            },
        depends=['product', 'state', 'company'])


class UpdateAssetStart(metaclass=PoolMeta):
    __name__ = 'account.asset.update.start'

    product = fields.Many2One('product.product', 'Product',
        states={
            'invisible': Bool(Eval('product', 1)),
            })
    company = fields.Many2One('company.company', 'Company',
        states={
            'invisible': Bool(Eval('company', 1)),
            })
    supplier_refund_invoice_line = fields.Many2One('account.invoice.line',
        'Supplier Refund Invoice Line',
        domain=[
            If(Eval('product', None) == None,
                ('product', '=', -1),
                ('product', '=', Eval('product', -1)),
                ),
            ('invoice.type', '=', 'in'),
            ['OR',
                ('quantity', '<', 0),
                ('unit_price', '<', 0),
                ],
            ['OR',
                ('company', '=', Eval('company', -1)),
                ('invoice.company', '=', Eval('company', -1)),
                ],
            ],
        depends=['product', 'company'])


class UpdateAsset(metaclass=PoolMeta):
    __name__ = 'account.asset.update'

    def default_start(self, fields):
        Asset = Pool().get('account.asset')

        asset = Asset(Transaction().context['active_id'])
        result = super().default_start(fields)
        result['product'] = asset.product.id
        result['company'] = asset.company.id
        return result

    def transition_create_lines(self):
        Asset = Pool().get('account.asset')

        asset = Asset(Transaction().context['active_id'])
        Asset.write([asset], {
                'supplier_refund_invoice_line':\
                    self.start.supplier_refund_invoice_line,
                })
        return super().transition_create_lines()

