import unittest

from lambda_function import *

class TestLambdaHandler(unittest.TestCase):
    def test_timestamp_to_date_string(self):
        '''
        Test timestamp_to_date_string function
        '''
        timestamp = 0
        result = timestamp_to_date_string(timestamp)
        self.assertEqual(result, '1970-1-1')

    def test_build_message(self):
        '''
        Test build_message function
        '''
        event = Message(serialNumber="abc123", event="connect", timestamp=0)
        msg = build_message(event)
        sn = event['serialNumber']
        ev = event['event']
        ts = event['timestamp']
        expected = '{"serialNumber": "%s", "event": "%s", "timestamp": %d}' % (sn, ev, ts)
        self.assertEqual(msg, expected)

    def test_build_s3_path(self):
        '''
        Test build_s3_path function
        '''
        event = Message(serialNumber="abc123", event="connect", timestamp=0)
        ts = event['timestamp']
        prefix = timestamp_to_date_string(ts)
        s3_path = build_s3_path(event)
        self.assertTrue(s3_path.startswith(prefix))

    def test_build_http_200(self):
        '''
        Test build_http_200 function
        '''
        event = Message(serialNumber="abc123", event="connect", timestamp=0)
        events = [event]
        http_response = build_http_200(events)
        status_code = http_response['statusCode']
        self.assertEqual(200, status_code)

    def test_build_http_400(self):
        '''
        Test build_http_400 function
        '''
        http_response = build_http_400()
        status_code = http_response['statusCode']
        self.assertEqual(400, status_code)

    def test_input_valid(self):
        '''
        Test is_input_valid function with valid input
        '''
        event = Message(serialNumber="abc123", event="connect", timestamp=0)
        valid = is_input_valid(event)
        self.assertTrue(valid)

    def test_input_invalid(self):
        '''
        Test is_input_valid function with invalid input
        '''
        self.assertFalse(is_input_valid('invalid input'))

if __name__ == '__main__':
    unittest.main()