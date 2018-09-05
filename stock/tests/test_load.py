import unittest

import os

from stock.create_table import create_table


class LoadAPITestCase(unittest.TestCase):
    def setUp(self):
        try:
            dynamo_table_name = os.environ['DYNAMODB_TABLE']
        except KeyError:
            os.environ['DYNAMODB_TABLE'] = test_table_name()
            create_table(os.environ['DYNAMODB_TABLE'])

    def test_get_feature(self):
        from stock.load import get_feature
        from stock.company import Company
        msft = Company("MSFT", "Microsoft", 100500)
        location = get_feature(msft)
        self.assertIsNot(location, None)

    def test_load(self):
        from stock.load import load
        load(None, None)

    def test_list(self):
        from stock.list import list
        response = list(None, None)
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.items())


def test_table_name():
    return 'test_table'


if __name__ == '__main__':
    create_table(test_table_name)
    unittest.main()
