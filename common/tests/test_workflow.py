import json
import os
import unittest
from unittest.mock import patch, Mock

import requests

from t5common.

class TestYourFunction(unittest.TestCase):

    @patch('requests.post')
    @patch('t5_common.utils.read_token')
    def test_your_function(self, mock_read_token, mock_post):
        # Mock requests for POST to Jira search endpoint
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'issues': [{'key': 'TEST-1234'}]}
        mock_post.return_value = mock_response

        mock_read_token_return = Mock()
        mock_read_token.return_value = '=======FAKETOKEN======='

        config = {
                'host': "https://taskforce5.atlassian.net",
                'user': "noone@lbl.gov",
                'token_file': "jira_token",
                'database': "jobs.db",
                'projects':[
                        {
                            'project': 'TEST',
                            'new_status': 'Fake Status',
                            'command': 'true'
                        }
                    ],
                }



        # Call the function that uses requests.post

        check_jira(config)

        breakpoint()

        # Assert the expected behavior
        #mock_post.assert_called_once_with('http://example.com/api', data={'key': 'value'})
        #self.assertEqual(result, expected_result)

