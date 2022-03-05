from flask import Flask, request
from flask_restful import Resource, Api

from utils.risk_calculator import RiskCalculator
from utils.vo_response import VOResponse

app = Flask(__name__)
api = Api(app)


class RiskAPI(Resource):

    @staticmethod
    def post():
        data = request.get_json()
        vo_risk = RiskCalculator.calculate(data)
        return VOResponse.main_response(
            data=vo_risk,
            code=VOResponse.OK
        ), 200


api.add_resource(RiskAPI, '/risk')

if __name__ == '__main__':
    app.run(debug=True)

# test POST request
# curl -H "Content-Type: application/json" -X POST -d '{"name": "Angel", "address": "Cuba"}'  http://127.0.0.1:5000
