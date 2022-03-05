# Flask API

Project to create a basic API to calculate the user’s insurance needs

Author:

    Angel Garcia (alejandromf27@gmail.com)

Project set up:

    1. Create a python virtual env (python3.8 was used)
    2. Install requirements: 
    
        $ cd gerald_risk_api
        $ pip install -r requirements.txt
    
    3. Run flask app

        $ python risk_api.py (Recommended Pycharm or VSCode)

Functionalities:

    Endpoint to get user insurance needs. 

    POST: http://127.0.0.1:5000/risk
    Content-Type: application/json

    Body:
    {
      "age": 35,
      "dependents": 2,
      "house": {"ownership_status": "mortgaged"},
      "income": 500,
      "marital_status": "married",
      "risk_questions": [0, 1, 0],
      "vehicle": {"year": 2018}
    }
    
    Response:
    {
        "results": {
            "auto": "economic",
            "disability": "economic",
            "home": "economic",
            "life": "economic"
        },
        "code": "200"
    }
