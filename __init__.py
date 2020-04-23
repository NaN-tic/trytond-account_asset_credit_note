# This file is part account_asset_credit_note module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import asset

def register():
    Pool.register(
        asset.Asset,
        asset.UpdateAssetStart,
        module='account_asset_credit_note', type_='model')
    Pool.register(
        asset.UpdateAsset,
        module='account_asset', type_='wizard')
