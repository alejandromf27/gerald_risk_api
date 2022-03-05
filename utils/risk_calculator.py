from utils.vo_response import VOResponse
import datetime


def risk_range(points):
    if points <= 0:
        return "economic"
    elif 1 <= points <= 2:
        return "regular"
    else:
        return "responsible"


class RiskCalculator:
    """ class to calculate the insurance risk """

    @staticmethod
    def calculate(data):
        """
        Function to calculate all risk points
        :param data: data from the api call
        :return: vo_risk_profile json
        """
        disability = ""
        auto = ""
        home = ""
        life = ""

        disability_point_risk = 0
        auto_point_risk = 0
        home_point_risk = 0
        life_point_risk = 0
        house = data.get('house', {"ownership_status": False})
        vehicle = data.get('vehicle', {'year': False})

        # check ineligible
        auto, disability, home, life = RiskCalculator.check_ineligible(auto, data, disability, home, house, life,
                                                                       vehicle)

        # check age risks
        auto_point_risk, disability_point_risk, home_point_risk, life_point_risk = RiskCalculator.check_age(
            auto_point_risk, data, disability_point_risk, home_point_risk, life_point_risk)

        # check income risks
        auto_point_risk, disability_point_risk, home_point_risk, life_point_risk = RiskCalculator.check_income(
            auto_point_risk, data, disability_point_risk, home_point_risk, life_point_risk)

        # check house ownership
        disability_point_risk, home_point_risk = RiskCalculator.check_ownership(disability_point_risk, home_point_risk,
                                                                                house)

        # check dependents risk
        disability_point_risk, life_point_risk = RiskCalculator.check_dependents(data, disability_point_risk,
                                                                                 life_point_risk)

        # check marital status rick
        disability_point_risk, life_point_risk = RiskCalculator.check_married(data, disability_point_risk,
                                                                              life_point_risk)
        # check vehicle risk
        auto_point_risk = RiskCalculator.check_vehicle(auto_point_risk, vehicle)

        # final conversion of insurance
        disability = risk_range(disability_point_risk) if disability == "" else disability
        auto = risk_range(auto_point_risk) if auto == "" else auto
        home = risk_range(home_point_risk) if home == "" else home
        life = risk_range(life_point_risk) if life == "" else life

        return VOResponse.vo_risk_profile(auto, disability, home, life)

    @staticmethod
    def check_vehicle(auto_point_risk, vehicle):
        """
        Function to check vehicle risk points
        :param auto_point_risk: auto risk points
        :param vehicle: vehicle year
        :return: final risk points added
        """
        if vehicle.get('year', None):
            now = datetime.datetime.now()
            if int(now.year) - int(vehicle.get('year')) <= 5:
                auto_point_risk += 1
        return auto_point_risk

    @staticmethod
    def check_married(data, disability_point_risk, life_point_risk):
        """
        Function to check marital status
        :param data: the info received from api call
        :param disability_point_risk: disability risk points
        :param life_point_risk: life risk points
        :return: final risk points added, deducted
        """
        if data.get('marital_status') == "married":
            life_point_risk += 1
            disability_point_risk -= 1
        return disability_point_risk, life_point_risk

    @staticmethod
    def check_dependents(data, disability_point_risk, life_point_risk):
        """
        Function to check dependent risk points
        :param data: the info received from api call
        :param disability_point_risk: disability risk points
        :param life_point_risk: life risk points
        :return: final risk points added
        """
        if data.get('dependents', 0) > 0:
            disability_point_risk += 1
            life_point_risk += 1
        return disability_point_risk, life_point_risk

    @staticmethod
    def check_ownership(disability_point_risk, home_point_risk, house):
        """
        Fucntion to check additional points because of mortgaged
        :param disability_point_risk: disability risk points
        :param home_point_risk: home risk points
        :param house: type of house
        :return: final risk points added
        """
        if house.get('ownership_status') == "mortgaged":
            home_point_risk += 1
            disability_point_risk += 1
        return disability_point_risk, home_point_risk

    @staticmethod
    def check_income(auto_point_risk, data, disability_point_risk, home_point_risk, life_point_risk):
        """
        Function to check income risk
        :param auto_point_risk: auto risk points
        :param data: the info received from api call
        :param disability_point_risk: disability risk points
        :param home_point_risk: home risk points
        :param life_point_risk: life risk points
        :return: final risk points deducted
        """
        if data.get('income', 0) > 200:
            disability_point_risk -= 1
            auto_point_risk -= 1
            home_point_risk -= 1
            life_point_risk -= 1
        return auto_point_risk, disability_point_risk, home_point_risk, life_point_risk

    @staticmethod
    def check_age(auto_point_risk, data, disability_point_risk, home_point_risk, life_point_risk):
        """
        Function to deduct points according age
        :param auto_point_risk: auto risk points
        :param data: the info received from api call
        :param disability_point_risk: disability risk points
        :param home_point_risk: home risk points
        :param life_point_risk: life risk points
        :return: final risk points deducted
        """
        if data.get('age', 0) < 30:
            disability_point_risk -= 2
            auto_point_risk -= 2
            home_point_risk -= 2
            life_point_risk -= 2
        elif 30 <= data.get('age', 0) <= 40:
            disability_point_risk -= 1
            auto_point_risk -= 1
            home_point_risk -= 1
            life_point_risk -= 1
        return auto_point_risk, disability_point_risk, home_point_risk, life_point_risk

    @staticmethod
    def check_ineligible(auto, data, disability, home, house, life, vehicle):
        """
        Check ineligible reasons
        :param auto: auto status
        :param data: the info received from api call
        :param disability: disability status
        :param home: home status
        :param house: house status
        :param life: life status
        :param vehicle: vehicle data with year
        :return: final status of auto, disability, home, life
        """
        if data.get('income', 0) == 0:
            disability = "ineligible"
        if house.get('ownership_status') not in ['owned', 'mortgaged']:
            home = "ineligible"
        if not vehicle.get('year', False):
            auto = "ineligible"
        if data.get('age', 0) > 60:
            disability = "ineligible"
            life = "ineligible"
        return auto, disability, home, life
