# This file is part of Tryton.  The COPYRIGHT file at the top level of this
# repository contains the full copyright notices and license terms.
from decimal import Decimal
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Asset']


class Asset(metaclass=PoolMeta):
    __name__ = 'account.asset'

    credit_note = fields.Boolean('Credit Note')

    @staticmethod
    def default_credit_note():
        return False

    def depreciate(self):
        """
        Returns all the depreciation amounts still to be accounted.
        """
        Line = Pool().get('account.asset.line')
        amounts = {}
        dates = self.compute_move_dates()
        amount = (self.value - self.get_depreciated_amount()
            - self.residual_value)
        if self.credit_note:
            if amount >= 0:
                return amounts
        else:
            if amount <= 0:
                return amounts
            return super().depreciate()

        residual_value, acc_depreciation = amount, Decimal(0)
        asset_line = None
        for date in dates:
            depreciation = self.compute_depreciation(date, dates)
            amounts[date] = asset_line = Line(
                acquired_value=self.value,
                depreciable_basis=amount,
                )
            if depreciation < residual_value:
                asset_line.depreciation = residual_value
                asset_line.accumulated_depreciation = (
                    self.get_depreciated_amount()
                    + acc_depreciation + residual_value)
                break
            else:
                residual_value -= depreciation
                acc_depreciation += depreciation
                asset_line.depreciation = depreciation
                asset_line.accumulated_depreciation = (
                    self.get_depreciated_amount() + acc_depreciation)
        else:
            if residual_value < 0 and asset_line is not None:
                asset_line.depreciation += residual_value
                asset_line.accumulated_depreciation += residual_value
        for asset_line in amounts.values():
            asset_line.actual_value = (self.value -
                asset_line.accumulated_depreciation)
        return amounts
