import ast
import json
import unittest

from risk_api import app


class TestApi(unittest.TestCase):

    def setUp(self) -> None:
        tester = app.test_client(self)
        info = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "mortgaged"},
            "income": 500,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }
        self.response = tester.post(
            '/risk',
            data=json.dumps(info),
            headers={'Content-Type': 'application/json'}
        )

    def test_content(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.content_type, "application/json")

    def test_data(self):
        expected_data = {
            "results": {
                "auto": "economic",
                "disability": "economic",
                "home": "economic",
                "life": "economic"
            },
            "code": "200"
        }
        byte_str = self.response.data
        dict_str = byte_str.decode("UTF-8")
        mydata = ast.literal_eval(dict_str)

        self.assertEqual(mydata, expected_data)


if __name__ == "__main__":
    unittest.main()