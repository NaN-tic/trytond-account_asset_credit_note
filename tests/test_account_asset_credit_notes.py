# This file is part account_asset_credit_note module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class AccountAssetCreditNotesTestCase(ModuleTestCase):
    'Test Account Asset Credit Notes module'
    module = 'account_asset_credit_note'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountAssetCreditNotesTestCase))
    return suite
