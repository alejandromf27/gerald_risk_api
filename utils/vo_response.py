class VOResponse:
    OK = '200'  # OK
    NOT_FOUND = '404'  # RECORD NOT FOUND

    @staticmethod
    def main_response(data=None, code=OK):
        return {
            'results': data,
            'code': code
        }

    @staticmethod
    def vo_risk_profile(auto="", disability="", home="", life=""):
        return {
            "auto": auto,
            "disability": disability,
            "home": home,
            "life": life
        }
