import unittest

from lambda_function import *

class TestLambdaHandler(unittest.TestCase):
    def test_timestamp_to_date_string(self):
        '''
        Test that it can ...
        '''
        timestamp = 0
        result = timestamp_to_date_string(timestamp)
        print(result)
        self.assertEqual(result, '1970-1-1')

if __name__ == '__main__':
    unittest.main()