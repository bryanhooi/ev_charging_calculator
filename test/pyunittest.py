from unittest import mock

from app.calculator import *
import unittest
import datetime
from unittest.mock import Mock, patch

class TestCalculator(unittest.TestCase):

    @patch('app.calculator.requests.get')
    def test_cost_calculation_surcharge_discount(self, mock_1):
        self.calculator = Calculator(5000, "14/09/2021")
        peak_time_holiday = datetime.datetime(2021, 9, 14, 10, 0, 0)
        non_peak_time_non_holiday = datetime.datetime(2021, 9, 12, 3, 0, 0)

        # Test case 1 : Test holiday (weekday), peak
        self.assertEqual(self.calculator.cost_calculation_surcharge_discount(peak_time_holiday, 10), (10, 1.1))
        
        # Test case 2 : Test non-holiday (weekend), non_peak
        self.assertEqual(self.calculator.cost_calculation_surcharge_discount(non_peak_time_non_holiday, 10), (5, 1))

    @patch('app.calculator.requests.get')
    def test_cost_v1(self, mock_2):
        self.calculator = Calculator(5000, "14/09/2021")
        # Test case 1 : start_time after 18, end_time next day before 6am, multiple hours, weekend, future date
        self.assertEqual(self.calculator.cost_calculation_v1(0, 100, 40, 10, 7.2, "12/09/2022", "23:55"), '-')

        # Test case 2 : start_time before peak, end_time before peak, single day
        self.assertEqual(self.calculator.cost_calculation_v1(0, 100, 20, 50, 350, "14/09/2021", "05:30"), 5.5)

        # Test case 3 : start_time before peak, end_time before off peak, single day, multiple hours
        self.assertEqual(self.calculator.cost_calculation_v1(0, 100, 40, 10, 7.2, "14/09/2021", "05:30"), 4.2)

        # Test case 4 : start_time after 6, end_time before 18, single day, single hour
        self.assertEqual(self.calculator.cost_calculation_v1(0, 100, 40, 50,350, "14/09/2021", "06:10"), 22.0)

        # Test case 5 : start_time after 6, end_time before 18, single day, multiple hours
        self.assertEqual(self.calculator.cost_calculation_v1(0, 100, 40, 10, 7.2, "14/09/2021", "06:10"), 4.4)

        # Test case 6 : start_time after 18, end_time after 18, single day, single hour
        self.assertEqual(self.calculator.cost_calculation_v1(0, 100, 40, 50, 350, "14/09/2021", "17:55"), 19.33)

        # Test case 7 : start_time after 18, end_time before 18, single day, multiple hours
        self.assertEqual(self.calculator.cost_calculation_v1(0, 100, 40, 10, 7.2, "14/09/2021", "19:00"), 2.2)

        # Test case 8 : start_time after 18, end_time after 18, single day, single hour, weekday
        self.assertEqual(self.calculator.cost_calculation_v1(0, 100, 40, 50, 350, "14/09/2021", "19:00"), 11)

        # Test case 9 : start_time after 18, end_time after 18, single day, single hour, weekend
        self.assertEqual(self.calculator.cost_calculation_v1(0, 100, 40, 50, 350, "12/09/2021", "23:55"), 10.24)

        # Test case 10 : start_time after 18, end_time next day before 6am, multiple hours, weekend
        self.assertEqual(self.calculator.cost_calculation_v1(0, 100, 40, 10, 7.2, "12/09/2021", "23:55"), 2.20)

        # Test case 11 : multiple hours, but no last hour
        self.assertEqual(self.calculator.cost_calculation_v1(0, 100, 150, 10, 50, "12/09/2021", "01:00"), 7.5)

    @mock.patch.object(Calculator, 'calculate_solar_energy_new', return_value=[])
    @patch('app.calculator.requests.get')
    def test_cost_v2(self, mock_2, mock_calculate_solar_energy_new):
        self.calculator = Calculator(5000, "14/09/2021")
        # Test case 1 : start_time after 18, end_time next day before 6am, multiple hours, weekend, future date
        self.assertEqual(self.calculator.cost_calculation_v2(0, 100, 40, 10, 7.2, "12/09/2022","23:55"), '-')
        
        mock_calculate_solar_energy_new.return_value = [[530, 533, 0.0]]
        # Test case 2 : start_time before peak, end_time before peak, single day
        self.assertEqual(self.calculator.cost_calculation_v2(0, 100, 20, 50, 350, "14/09/2021", "05:30"), 5.5)

        mock_calculate_solar_energy_new.return_value = [[530, 600, 0.0], [600, 700, 2.134837799717913], [700, 800, 3.0803949224259526], [800, 900, 3.1819464033850493], [900, 1000, 3.283497884344147], [1000, 1100, 3.3173483779971793], [1100, 1103, 0.1675599435825106]]
        # Test case 3 : start_time before peak, end_time before off peak, single day, multiple hours
        self.assertEqual(self.calculator.cost_calculation_v2(0, 100, 40, 10, 7.2, "14/09/2021", "05:30"), 2.53)

        mock_calculate_solar_energy_new.return_value = [[610, 616, 0.0]]
        # Test case 4 : start_time after 6, end_time before 18, single day, single hour
        self.assertEqual(self.calculator.cost_calculation_v2(0, 100, 40, 50, 350, "14/09/2021", "06:10"), 22.0)

        mock_calculate_solar_energy_new.return_value = [[610, 700, 2.134837799717913], [700, 800, 3.0803949224259526], [800, 900, 3.1819464033850493], [900, 1000, 3.283497884344147], [1000, 1100, 3.3173483779971793], [1100, 1143, 2.4016925246826517]]
        # Test case 5 : start_time after 6, end_time before 18, single day, multiple hours
        self.assertEqual(self.calculator.cost_calculation_v2(0, 100, 40, 10, 7.2, "14/09/2021", "06:10"), 2.49)

        mock_calculate_solar_energy_new.return_value =[[1755, 1800, 0.2708039492242595], [1800, 1801, 0.05246826516220028]]
        # Test case 6 : start_time after 6, end_time after 18, single day, single hour
        self.assertEqual(self.calculator.cost_calculation_v2(0, 100, 40, 50, 350, "14/09/2021", "17:55"), 19.17)

        # Test case 7 : start_time after 18, end_time before 18, single day, multiple hours
        mock_calculate_solar_energy_new.return_value = [[1900, 2000, 0.0], [2000, 2100, 0.0], [2100, 2200, 0.0], [2200, 2300, 0.0], [2300, 2359, 0.0], [0, 33, 0.0]]
        self.assertEqual(self.calculator.cost_calculation_v2(0, 100, 40, 10, 7.2, "14/09/2021", "19:00"), 2.2)

        mock_calculate_solar_energy_new.return_value = [[1900, 1906, 0.0]]
        # Test case 8 : start_time after 18, end_time after 18, single day, single hour
        self.assertEqual(self.calculator.cost_calculation_v2(0, 100, 40, 50, 350, "14/09/2021", "19:00"), 11)

        mock_calculate_solar_energy_new.return_value = [[2355, 2359, 0.0], [0, 1, 0.0]]
        # Test case  9 : start_time after 18, end_time after 18, single day, single hour
        self.assertEqual(self.calculator.cost_calculation_v2(0, 100, 40, 50, 350, "12/09/2021", "23:55"), 10.24)

        mock_calculate_solar_energy_new.return_value = [[2355, 2359, 0.0], [0, 100, 0.0], [100, 200, 0.0], [200, 300, 0.0], [300, 400, 0.0], [400, 500, 0.0], [500, 528, 0.0]]
        # Test case 10 : start_time after 18, end_time next day, multiple hours
        self.assertEqual(self.calculator.cost_calculation_v2(0, 100, 40, 10, 7.2, "12/09/2021", "23:55"), 2.20)

        mock_calculate_solar_energy_new.return_value = [[100, 200, 0.0],[200, 300, 0.0],[300, 400, 0.0]]
        # Test case 11 : multiple hours, but no last hour
        self.assertEqual(self.calculator.cost_calculation_v2(0, 100, 150, 10, 50, "12/09/2021", "01:00"), 7.5)

    @mock.patch.object(Calculator, 'calculate_solar_energy_new_w_cc', return_value=[])
    @patch('app.calculator.requests.get')
    def test_cost_v3(self, mock_2, mock_calculate_solar_energy_new_w_cc):
        self.calculator = Calculator(5000, "14/09/2021")
        
        mock_calculate_solar_energy_new_w_cc.return_value = [[[530, 533, 0.0]]]
        # start_time before peak, end_time before peak, single day
        self.assertEqual(self.calculator.cost_calculation_v3(0, 100, 20, 50, 350, "14/09/2021", "05:30"), 5.5)

        mock_calculate_solar_energy_new_w_cc.return_value = [[[530, 600, 0.0], [600, 700, 2.134837799717913], [700, 800, 3.0803949224259526], [800, 900, 3.1819464033850493], [900, 1000, 3.283497884344147], [1000, 1100, 3.3173483779971793], [1100, 1103, 0.1675599435825106]]]
        # start_time before peak, end_time before off peak, single day, multiple hours
        self.assertEqual(self.calculator.cost_calculation_v3(0, 100, 40, 10, 7.2, "14/09/2021", "05:30"), 2.53)

        mock_calculate_solar_energy_new_w_cc.return_value = [[[610, 616, 0.0]]]
        # start_time after 6, end_time before 18, single day, single hour
        self.assertEqual(self.calculator.cost_calculation_v3(0, 100, 40, 50, 350, "14/09/2021", "06:10"), 22.0)

        mock_calculate_solar_energy_new_w_cc.return_value = [[[610, 700, 2.134837799717913], [700, 800, 3.0803949224259526], [800, 900, 3.1819464033850493], [900, 1000, 3.283497884344147], [1000, 1100, 3.3173483779971793], [1100, 1143, 2.4016925246826517]]]
        # start_time after 6, end_time before 18, single day, multiple hours
        self.assertEqual(self.calculator.cost_calculation_v3(0, 100, 40, 10, 7.2, "14/09/2021", "06:10"), 2.49)

        mock_calculate_solar_energy_new_w_cc.return_value = [[[1755, 1800, 0.2708039492242595], [1800, 1801, 0.05246826516220028]]]
        # start_time after 6, end_time after 18, single day, single hour
        self.assertEqual(self.calculator.cost_calculation_v3(0, 100, 40, 50, 350, "14/09/2021", "17:55"), 19.17)

        # start_time after 18, end_time before 18, single day, multiple hours
        mock_calculate_solar_energy_new_w_cc.return_value = [[[1900, 2000, 0.0], [2000, 2100, 0.0], [2100, 2200, 0.0], [2200, 2300, 0.0], [2300, 2359, 0.0], [0, 33, 0.0]]]
        self.assertEqual(self.calculator.cost_calculation_v3(0, 100, 40, 10, 7.2, "14/09/2021", "19:00"), 2.2)

        mock_calculate_solar_energy_new_w_cc.return_value = [[[1900, 1906, 0.0]]]
        # start_time after 18, end_time after 18, single day, single hour
        self.assertEqual(self.calculator.cost_calculation_v3(0, 100, 40, 50, 350, "14/09/2021", "19:00"), 11)

        mock_calculate_solar_energy_new_w_cc.return_value = [[[2355, 2359, 0.0], [0, 1, 0.0]]]
        # start_time after 18, end_time after 18, single day, single hour
        self.assertEqual(self.calculator.cost_calculation_v3(0, 100, 40, 50, 350, "12/09/2021", "23:55"), 10.24)

        mock_calculate_solar_energy_new_w_cc.return_value = [[[2355, 2359, 0.0], [0, 100, 0.0], [100, 200, 0.0], [200, 300, 0.0], [300, 400, 0.0], [400, 500, 0.0], [500, 528, 0.0]]]
        # start_time after 18, end_time next day, multiple hours
        self.assertEqual(self.calculator.cost_calculation_v3(0, 100, 40, 10, 7.2, "12/09/2021", "23:55"), 2.20)

        mock_calculate_solar_energy_new_w_cc.return_value = [[[2355, 2359, 0.0], [0, 100, 0.0], [100, 200, 0.0], [200, 300, 0.0], [300, 400, 0.0], [400, 500, 0.0], [500, 528, 0.0]], [[2355, 2359, 0.0], [0, 100, 0.0], [100, 200, 0.0], [200, 300, 0.0], [300, 400, 0.0], [400, 500, 0.0], [500, 528, 0.0]], [[2355, 2359, 0.0], [0, 100, 0.0], [100, 200, 0.0], [200, 300, 0.0], [300, 400, 0.0], [400, 500, 0.0], [500, 528, 0.0]]]
        # start_time after 18, end_time next day, multiple hours, future date
        self.assertEqual(self.calculator.cost_calculation_v3(0, 100, 40, 10, 7.2, "12/09/2022", "23:55"), 2.20)


        mock_calculate_solar_energy_new_w_cc.return_value = [[[100, 200, 0.0],[200, 300, 0.0],[300, 400, 0.0]]]
        # multiple hours, but no last hour
        self.assertEqual(self.calculator.cost_calculation_v3(0, 100, 150, 10, 50, "12/09/2021", "01:00"), 7.5)

    @patch('app.calculator.requests.get')
    def test_calculate_solar_energy_new_single_day(self, mock_1):
        self.calculator = Calculator(7250, "22/02/2021")
        self.calculator.location_id = "22d72902-b72f-4ca0-a522-4dbfb77a7b78"
        mock_1.return_value.json.return_value = {'date': '2021-02-22', 'sunrise': '05:44:00', 'sunset': '19:06:00', 'moonrise': '15:43:00', 'moonset': '00:01:00', 'moonPhase': 'Waxing Gibbous', 'moonIlluminationPct': 73, 'minTempC': 9, 'maxTempC': 21, 'avgTempC': 17, 'sunHours': 5.3, 'uvIndex': 5, 'location': {'id': '22d72902-b72f-4ca0-a522-4dbfb77a7b78', 'postcode': '7250', 'name': 'BLACKSTONE HEIGHTS', 'state': 'TAS', 'latitude': '-41.46', 'longitude': '147.0820001', 'distanceToNearestWeatherStationMetres': 5607.391317385195, 'nearestWeatherStation': {'name': 'LAUNCESTON (TI TREE BEND)', 'state': 'TAS', 'latitude': '-41.4194', 'longitude': '147.1219'}}, 'hourlyWeatherHistory': [
            {'hour': 0, 'tempC': 13, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 1, 'uvIndex': 1, 'windspeedKph': 2, 'windDirectionDeg': 232, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 89, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 1, 'tempC': 12, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 3, 'uvIndex': 1, 'windspeedKph': 2, 'windDirectionDeg': 258, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 91, 'visibilityKm': 8, 'pressureMb': 1007},
            {'hour': 2, 'tempC': 11, 'weatherDesc': 'Clear', 'cloudCoverPct': 6, 'uvIndex': 1, 'windspeedKph': 3, 'windDirectionDeg': 284, 'windDirectionCompass': 'WNW', 'precipitationMm': 0, 'humidityPct': 93, 'visibilityKm': 6, 'pressureMb': 1006},
            {'hour': 3, 'tempC': 9, 'weatherDesc': 'Clear', 'cloudCoverPct': 9, 'uvIndex': 1, 'windspeedKph': 3, 'windDirectionDeg': 310, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 95, 'visibilityKm': 5, 'pressureMb': 1006},
            {'hour': 4, 'tempC': 10, 'weatherDesc': 'Clear', 'cloudCoverPct': 7, 'uvIndex': 1, 'windspeedKph': 4, 'windDirectionDeg': 314, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 93, 'visibilityKm': 6, 'pressureMb': 1006},
            {'hour': 5, 'tempC': 10, 'weatherDesc': 'Mist', 'cloudCoverPct': 6, 'uvIndex': 1, 'windspeedKph': 4, 'windDirectionDeg': 319, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 90, 'visibilityKm': 6, 'pressureMb': 1006},
            {'hour': 6, 'tempC': 10, 'weatherDesc': 'Mist', 'cloudCoverPct': 4, 'uvIndex': 3, 'windspeedKph': 4, 'windDirectionDeg': 324, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 88, 'visibilityKm': 7, 'pressureMb': 1007},
            {'hour': 7, 'tempC': 12, 'weatherDesc': 'Mist', 'cloudCoverPct': 3, 'uvIndex': 3, 'windspeedKph': 6, 'windDirectionDeg': 313, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 78, 'visibilityKm': 8, 'pressureMb': 1007},
            {'hour': 8, 'tempC': 14, 'weatherDesc': 'Sunny', 'cloudCoverPct': 1, 'uvIndex': 4, 'windspeedKph': 7, 'windDirectionDeg': 303, 'windDirectionCompass': 'WNW', 'precipitationMm': 0, 'humidityPct': 68, 'visibilityKm': 9, 'pressureMb': 1007},
            {'hour': 9, 'tempC': 16, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 8, 'windDirectionDeg': 292, 'windDirectionCompass': 'WNW', 'precipitationMm': 0, 'humidityPct': 58, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 10, 'tempC': 18, 'weatherDesc': 'Sunny', 'cloudCoverPct': 6, 'uvIndex': 5, 'windspeedKph': 10, 'windDirectionDeg': 286, 'windDirectionCompass': 'WNW', 'precipitationMm': 0, 'humidityPct': 52, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 11, 'tempC': 19, 'weatherDesc': 'Sunny', 'cloudCoverPct': 12, 'uvIndex': 5, 'windspeedKph': 11, 'windDirectionDeg': 281, 'windDirectionCompass': 'W', 'precipitationMm': 0, 'humidityPct': 45, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 12, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 17, 'uvIndex': 6, 'windspeedKph': 13, 'windDirectionDeg': 275, 'windDirectionCompass': 'W', 'precipitationMm': 0, 'humidityPct': 39, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 13, 'tempC': 20, 'weatherDesc': 'Sunny', 'cloudCoverPct': 19, 'uvIndex': 6, 'windspeedKph': 14, 'windDirectionDeg': 270, 'windDirectionCompass': 'W', 'precipitationMm': 0, 'humidityPct': 38, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 14, 'tempC': 20, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 20, 'uvIndex': 5, 'windspeedKph': 15, 'windDirectionDeg': 264, 'windDirectionCompass': 'W', 'precipitationMm': 0, 'humidityPct': 38, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 15, 'tempC': 20, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 22, 'uvIndex': 5, 'windspeedKph': 16, 'windDirectionDeg': 259, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 37, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 16, 'tempC': 18, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 20, 'uvIndex': 5, 'windspeedKph': 15, 'windDirectionDeg': 255, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 39, 'visibilityKm': 10, 'pressureMb': 1008},
            {'hour': 17, 'tempC': 17, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 18, 'uvIndex': 5, 'windspeedKph': 14, 'windDirectionDeg': 251, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 42, 'visibilityKm': 10, 'pressureMb': 1008},
            {'hour': 18, 'tempC': 16, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 16, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 247, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 44, 'visibilityKm': 10, 'pressureMb': 1009},
            {'hour': 19, 'tempC': 15, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 14, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 237, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 50, 'visibilityKm': 10, 'pressureMb': 1010},
            {'hour': 20, 'tempC': 13, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 11, 'uvIndex': 1, 'windspeedKph': 9, 'windDirectionDeg': 227, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 55, 'visibilityKm': 10, 'pressureMb': 1011},
            {'hour': 21, 'tempC': 12, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 9, 'uvIndex': 1, 'windspeedKph': 7, 'windDirectionDeg': 217, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 60, 'visibilityKm': 10, 'pressureMb': 1012},
            {'hour': 22, 'tempC': 11, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 7, 'uvIndex': 1, 'windspeedKph': 6, 'windDirectionDeg': 212, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 64, 'visibilityKm': 10, 'pressureMb': 1012},
            {'hour': 23, 'tempC': 9, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 5, 'uvIndex': 1, 'windspeedKph': 4, 'windDirectionDeg': 207, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 68, 'visibilityKm': 10, 'pressureMb': 1012}]}

        def s_p (hour,api):
            sunset = datetime.datetime.strptime(api['sunset'], "%H:%M:%S")
            sunrise = datetime.datetime.strptime(api['sunrise'], "%H:%M:%S")
            if sunset.minute < sunrise.minute:
                sunset -= timedelta(hours=1)
                dl = (sunset.hour - sunrise.hour) + (sunset.minute + 60 - sunrise.minute) / 60
            else :
                dl = (sunset.hour - sunrise.hour) + (sunset.minute - sunrise.minute) / 60

            return round(api['sunHours'] * (hour / dl) * 50 * 0.20, 11)

        # single day
        self.assertEqual(self.calculator.calculate_solar_energy_new(start_date="22/02/2021",
                                                        start_time="10:00",
                                                        initial_state=0,
                                                        final_state=100,
                                                        capacity=20, power=2), [[1000, 1100, s_p(1, mock_1.return_value.json())], [1100, 1200, s_p(1, mock_1.return_value.json())], [1200, 1300, s_p(1, mock_1.return_value.json())], [1300, 1400, s_p(1, mock_1.return_value.json())], [1400, 1500, s_p(1, mock_1.return_value.json())], [1500, 1600, s_p(1, mock_1.return_value.json())], [1600, 1700, s_p(1, mock_1.return_value.json())], [1700, 1800, s_p(1, mock_1.return_value.json())], [1800, 1900, s_p(1, mock_1.return_value.json())], [1900, 2000, s_p(0.1, mock_1.return_value.json())], [2000, 2000, 0.0]])
        
        # future date
        self.assertRaises(AssertionError, lambda: self.calculator.calculate_solar_energy_new(start_date="22/02/2022",
                                                                    start_time="10:00",
                                                                    initial_state=0,
                                                                    final_state=100,
                                                                    capacity=20, power=2))

    @patch('app.calculator.requests.get')
    @mock.patch.object(Calculator, 'calculate_solar_energy_within_a_day_by_hour', return_value=[])
    def test_calculate_solar_energy_new_multiple_day(self, mock_1, mock_2):
        self.calculator = Calculator(7250, "22/02/2021")
        self.calculator.location_id = "22d72902-b72f-4ca0-a522-4dbfb77a7b78"
        
        # multiple days
        multiple_day_1_api_rtn = [[2000, 2100, 0.0], [2100, 2200, 0.0], [2200, 2300, 0.0], [2300, 2359, 0.0]]
        multiple_day_2_api_rtn = [[0, 100, 0.0], [100, 200, 0.0], [200, 300, 0.0], [300, 400, 0.0], [400, 500, 0.0], [500, 600, 1.07008760951], [600, 600, 0.0]]

        mock_1.side_effect = [multiple_day_1_api_rtn , multiple_day_2_api_rtn]
        self.assertEqual(self.calculator.calculate_solar_energy_new(start_date="22/02/2021",
                                                                    start_time="20:00",
                                                                    initial_state=0,
                                                                    final_state=100,
                                                                    capacity=20, power=2), multiple_day_1_api_rtn + multiple_day_2_api_rtn)

    @patch('app.calculator.requests.get')
    def test_calculate_solar_energy_new_w_cc(self, mock1):
        self.calculator = Calculator(7250, "22/02/2020", "Launceston")
        self.calculator.location_id = "5998b29a-8e3d-4c1e-857c-b5dce80eea6d"

        json_output2020 = {'date': '2020-02-22', 'sunrise': '05:43:00', 'sunset': '19:07:00',
                           'moonrise': '03:51:00', 'moonset': '18:41:00', 'moonPhase': 'New Moon',
                           'moonIlluminationPct': 0, 'minTempC': 8, 'maxTempC': 20, 'avgTempC': 17,
                           'sunHours': 6.7, 'uvIndex': 5,
                           'location':
                               {'id': '5998b29a-8e3d-4c1e-857c-b5dce80eea6d', 'postcode': '7250',
                                'name': 'LAUNCESTON', 'state': 'TAS',
                                'latitude': '-41.4332215', 'longitude': '147.1440875',
                                'distanceToNearestWeatherStationMetres': 2323.920987503416,
                                'nearestWeatherStation': {'name': 'HOBLERS BRIDGE (NORTH ESK RIVER)', 'state': 'TAS',
                                                          'latitude': '-41.4392', 'longitude': '147.1708'}
                                },
                           'hourlyWeatherHistory': [
                               {'hour': 0, 'tempC': 9, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 17,
                                'uvIndex': 1,
                                'windspeedKph': 4, 'windDirectionDeg': 134, 'windDirectionCompass': 'SE',
                                'precipitationMm': 0, 'humidityPct': 78, 'visibilityKm': 10, 'pressureMb': 1023},
                               {'hour': 1, 'tempC': 9, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 19,
                                'uvIndex': 1,
                                'windspeedKph': 4, 'windDirectionDeg': 137, 'windDirectionCompass': 'SE',
                                'precipitationMm': 0, 'humidityPct': 80, 'visibilityKm': 10, 'pressureMb': 1023},
                               {'hour': 2, 'tempC': 8, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 21,
                                'uvIndex': 1,
                                'windspeedKph': 3, 'windDirectionDeg': 140, 'windDirectionCompass': 'SE',
                                'precipitationMm': 0, 'humidityPct': 83, 'visibilityKm': 10, 'pressureMb': 1023},
                               {'hour': 3, 'tempC': 8, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 23,
                                'uvIndex': 1,
                                'windspeedKph': 3, 'windDirectionDeg': 142, 'windDirectionCompass': 'SE',
                                'precipitationMm': 0, 'humidityPct': 85, 'visibilityKm': 10, 'pressureMb': 1023},
                               {'hour': 4, 'tempC': 8, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 24,
                                'uvIndex': 1,
                                'windspeedKph': 3, 'windDirectionDeg': 143, 'windDirectionCompass': 'SE',
                                'precipitationMm': 0, 'humidityPct': 84, 'visibilityKm': 10, 'pressureMb': 1023},
                               {'hour': 5, 'tempC': 9, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 25,
                                'uvIndex': 1,
                                'windspeedKph': 2, 'windDirectionDeg': 143, 'windDirectionCompass': 'SE',
                                'precipitationMm': 0, 'humidityPct': 82, 'visibilityKm': 10, 'pressureMb': 1024},
                               {'hour': 6, 'tempC': 9, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 26,
                                'uvIndex': 3,
                                'windspeedKph': 2, 'windDirectionDeg': 144, 'windDirectionCompass': 'SE',
                                'precipitationMm': 0, 'humidityPct': 81, 'visibilityKm': 10, 'pressureMb': 1024},
                               {'hour': 7, 'tempC': 11, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 25,
                                'uvIndex': 4,
                                'windspeedKph': 4, 'windDirectionDeg': 184, 'windDirectionCompass': 'S',
                                'precipitationMm': 0, 'humidityPct': 75, 'visibilityKm': 10, 'pressureMb': 1024},
                               {'hour': 8, 'tempC': 13, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 23,
                                'uvIndex': 4,
                                'windspeedKph': 5, 'windDirectionDeg': 225, 'windDirectionCompass': 'SW',
                                'precipitationMm': 0, 'humidityPct': 68, 'visibilityKm': 10, 'pressureMb': 1024},
                               {'hour': 9, 'tempC': 15, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 21,
                                'uvIndex': 5,
                                'windspeedKph': 6, 'windDirectionDeg': 266, 'windDirectionCompass': 'W',
                                'precipitationMm': 0, 'humidityPct': 62, 'visibilityKm': 10, 'pressureMb': 1024},
                               {'hour': 10, 'tempC': 17, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 21,
                                'uvIndex': 5,
                                'windspeedKph': 8, 'windDirectionDeg': 286, 'windDirectionCompass': 'WNW',
                                'precipitationMm': 0, 'humidityPct': 58, 'visibilityKm': 10, 'pressureMb': 1024},
                               {'hour': 11, 'tempC': 18, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 21,
                                'uvIndex': 5,
                                'windspeedKph': 10, 'windDirectionDeg': 307, 'windDirectionCompass': 'NW',
                                'precipitationMm': 0, 'humidityPct': 53, 'visibilityKm': 10, 'pressureMb': 1024},
                               {'hour': 12, 'tempC': 20, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 21,
                                'uvIndex': 5,
                                'windspeedKph': 11, 'windDirectionDeg': 327, 'windDirectionCompass': 'NNW',
                                'precipitationMm': 0, 'humidityPct': 49, 'visibilityKm': 10, 'pressureMb': 1023},
                               {'hour': 13, 'tempC': 20, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 17,
                                'uvIndex': 5,
                                'windspeedKph': 12, 'windDirectionDeg': 328, 'windDirectionCompass': 'NNW',
                                'precipitationMm': 0, 'humidityPct': 48, 'visibilityKm': 10, 'pressureMb': 1023},
                               {'hour': 14, 'tempC': 20, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 12,
                                'uvIndex': 5,
                                'windspeedKph': 13, 'windDirectionDeg': 329, 'windDirectionCompass': 'NNW',
                                'precipitationMm': 0, 'humidityPct': 48, 'visibilityKm': 10, 'pressureMb': 1022},
                               {'hour': 15, 'tempC': 20, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 7,
                                'uvIndex': 6,
                                'windspeedKph': 14, 'windDirectionDeg': 330, 'windDirectionCompass': 'NNW',
                                'precipitationMm': 0, 'humidityPct': 47, 'visibilityKm': 10, 'pressureMb': 1022},
                               {'hour': 16, 'tempC': 19, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 5,
                                'uvIndex': 5,
                                'windspeedKph': 13, 'windDirectionDeg': 332, 'windDirectionCompass': 'NNW',
                                'precipitationMm': 0, 'humidityPct': 53, 'visibilityKm': 10, 'pressureMb': 1022},
                               {'hour': 17, 'tempC': 19, 'weatherDesc': 'Sunny', 'cloudCoverPct': 2, 'uvIndex': 5,
                                'windspeedKph': 12, 'windDirectionDeg': 334, 'windDirectionCompass': 'NNW',
                                'precipitationMm': 0, 'humidityPct': 58, 'visibilityKm': 10, 'pressureMb': 1022},
                               {'hour': 18, 'tempC': 18, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1,
                                'windspeedKph': 11, 'windDirectionDeg': 336, 'windDirectionCompass': 'NNW',
                                'precipitationMm': 0, 'humidityPct': 64, 'visibilityKm': 10, 'pressureMb': 1022},
                               {'hour': 19, 'tempC': 18, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1,
                                'windspeedKph': 9, 'windDirectionDeg': 341, 'windDirectionCompass': 'NNW',
                                'precipitationMm': 0, 'humidityPct': 71, 'visibilityKm': 10, 'pressureMb': 1022},
                               {'hour': 20, 'tempC': 17, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1,
                                'windspeedKph': 7, 'windDirectionDeg': 345, 'windDirectionCompass': 'NNW',
                                'precipitationMm': 0, 'humidityPct': 78, 'visibilityKm': 10, 'pressureMb': 1022},
                               {'hour': 21, 'tempC': 16, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1,
                                'windspeedKph': 5, 'windDirectionDeg': 350, 'windDirectionCompass': 'N',
                                'precipitationMm': 0, 'humidityPct': 85, 'visibilityKm': 10, 'pressureMb': 1023},
                               {'hour': 22, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 15, 'uvIndex': 1,
                                'windspeedKph': 4, 'windDirectionDeg': 235, 'windDirectionCompass': 'SW',
                                'precipitationMm': 0, 'humidityPct': 88, 'visibilityKm': 8, 'pressureMb': 1023},
                               {'hour': 23, 'tempC': 13, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 31,
                                'uvIndex': 1,
                                'windspeedKph': 3, 'windDirectionDeg': 120, 'windDirectionCompass': 'ESE',
                                'precipitationMm': 0, 'humidityPct': 90, 'visibilityKm': 6, 'pressureMb': 1023}
                           ]}

        mock1.return_value.json.return_value = json_output2020

        # Current_date <= max_date_allowed, charging time within a day
        self.assertEqual(
            [[[1700, 1800, 4.9], [1800, 1800, 0]]],
            self.calculator.calculate_solar_energy_new_w_cc(start_date="22/02/2020", start_time="17:00",
                                                            initial_state=0, final_state=50,
                                                            capacity=4, power=2.0)
        )

    def test_calculate_solar_energy_new_w_cc_wo_mocking(self):
        self.calculator = Calculator(7250, "22/02/2021", "Launceston")

        # current_date <= max_date_allowed, charging time not within a day
        self.assertEqual(
            [[[2300, 2359, 0.0], [0000, 100, 0.0], [100,100,0.0]]],
            self.calculator.calculate_solar_energy_new_w_cc(start_date="22/02/2021", start_time="23:00",
                                                            initial_state=0, final_state=100,
                                                            capacity=4, power=2.0)
        )

        # current_date > max_date_allowed, ref_date <= current_date, charging time within a day
        self.calculator = Calculator(7250, "22/02/2022", "Launceston")
        self.assertEqual(
            [
                [[1700, 1800, 3.55810473815], [1800, 1800, 0]],
                [[1700, 1800, 4.9], [1800, 1800, 0.0]],
                [[1700, 1800, 3.25180572852], [1800, 1800, 0.0]],
            ],
            self.calculator.calculate_solar_energy_new_w_cc(start_date="22/02/2022", start_time="17:00",
                                                            initial_state=0, final_state=50,
                                                            capacity=4, power=2.0)
        )

        # current_date > max_date_allowed, ref_date > current_date, charging time within a day
        self.calculator = Calculator(7250, "25/12/2022", "Launceston")
        self.assertEqual(
            [
                [[1700, 1800, 5.04105378705], [1800, 1800, 0]],
                [[1700, 1800, 5.21097694841], [1800, 1800, 0.0]],
                [[1700, 1800, 4.15850713502], [1800, 1800, 0.0]],
            ],
            self.calculator.calculate_solar_energy_new_w_cc(start_date="25/12/2022", start_time="17:00",
                                                            initial_state=0, final_state=50,
                                                            capacity=4, power=2.0)
        )

    @patch('app.calculator.requests.get')
    def test_time_calculation(self, mock):
        self.calculator = Calculator(5000, "14/09/2021")

        # randomly generated test cases with one per available charger configuration
        self.assertEqual(self.calculator.time_calculation(23, 92, 73, 2.0), 25.18)    # configuration 1
        self.assertEqual(self.calculator.time_calculation(29, 37, 42, 3.6), 0.93)     # configuration 2
        self.assertEqual(self.calculator.time_calculation(14, 52, 50, 7.2), 2.64)     # configuration 3
        self.assertEqual(self.calculator.time_calculation(2, 10, 80, 11), 0.58)       # configuration 4
        self.assertEqual(self.calculator.time_calculation(50, 80, 100, 22), 1.36)     # configuration 5
        self.assertEqual(self.calculator.time_calculation(7, 83, 56, 36), 1.18)       # configuration 6
        self.assertEqual(self.calculator.time_calculation(10, 25, 40, 90), 0.07)      # configuration 7
        self.assertEqual(self.calculator.time_calculation(5, 95, 150, 350), 0.39)     # configuration 8

    @patch('app.calculator.requests.get')
    def test_is_holiday_v2(self, mock):
        self.calculator = Calculator(5000, "14/09/2021")

        # test for non-holidays that are on weekends
        self.assertEqual(self.calculator.is_holiday_v2(datetime.datetime(2020, 9, 19)), False)  # non-holiday on a Saturday
        self.assertEqual(self.calculator.is_holiday_v2(datetime.datetime(2020, 5, 17)), False)  # non-holiday on a Sunday

        # test for non-holidays that are on weekdays
        self.assertEqual(self.calculator.is_holiday_v2(datetime.datetime(2020, 8, 17)), True)   # non-holiday on a Monday
        self.assertEqual(self.calculator.is_holiday_v2(datetime.datetime(2020, 8, 21)), True)   # non-holoday on a Friday

        # test for holidays that are on weekends
        self.assertEqual(self.calculator.is_holiday_v2(datetime.datetime(2021, 4, 25)), True)   # Anzac Day on a Sunday
        self.assertEqual(self.calculator.is_holiday_v2(datetime.datetime(2021, 12, 25)), True)  # Christmas Day on a Saturday

        # test for holidays that are on weekdays
        self.assertEqual(self.calculator.is_holiday_v2(datetime.datetime(2021, 10, 4)), True)   # Labour Day on a Monday
        self.assertEqual(self.calculator.is_holiday_v2(datetime.datetime(2021, 1, 26)), True)   # Australia Day on a Tuesday

    @patch('app.calculator.requests.get')
    def test_is_peak_v2(self, mock):
        self.calculator = Calculator(5000, "14/09/2021")

        # 2 tests for times within peak hours
        self.assertEqual(self.calculator.is_peak_v2(datetime.datetime(2008, 12, 1, 14, 4)), True)
        self.assertEqual(self.calculator.is_peak_v2(datetime.datetime(2008, 12, 1, 16, 6)), True)

        # 2 tests for times outside peak hours
        self.assertEqual(self.calculator.is_peak_v2(datetime.datetime(2008, 12, 1, 5, 40)), False)
        self.assertEqual(self.calculator.is_peak_v2(datetime.datetime(2008, 12, 1, 20, 45)), False)

        # 2 tests for times directly on peak hour thresholds
        self.assertEqual(self.calculator.is_peak_v2(datetime.datetime(2008, 12, 1, 6, 0)), True)
        self.assertEqual(self.calculator.is_peak_v2(datetime.datetime(2008, 12, 1, 18, 0)), True)

    @patch('app.calculator.requests.get')
    def test_get_power(self, mock):
        self.calculator = Calculator(5000, "14/09/2021")
        # test case for power output of each possible charger configuration
        self.assertEqual(self.calculator.get_power(1), 2.0)
        self.assertEqual(self.calculator.get_power(2), 3.6)
        self.assertEqual(self.calculator.get_power(3), 7.2)
        self.assertEqual(self.calculator.get_power(4), 11)
        self.assertEqual(self.calculator.get_power(5), 22)
        self.assertEqual(self.calculator.get_power(6), 36)
        self.assertEqual(self.calculator.get_power(7), 90)
        self.assertEqual(self.calculator.get_power(8), 350)
        self.assertRaises(AssertionError,lambda: self.calculator.get_power(9))
        self.assertRaises(AssertionError,lambda: self.calculator.get_power("abc"))
        self.assertRaises(AssertionError,lambda: self.calculator.get_power("wow"))

    @patch('app.calculator.requests.get')
    def test_get_price(self, mock):
        self.calculator = Calculator(5000, "14/09/2021")

        # test case for price of each possible charger configuration
        self.assertEqual(self.calculator.get_price(1), 5)
        self.assertEqual(self.calculator.get_price(2), 7.5)
        self.assertEqual(self.calculator.get_price(3), 10)
        self.assertEqual(self.calculator.get_price(4), 12.5)
        self.assertEqual(self.calculator.get_price(5), 15)
        self.assertEqual(self.calculator.get_price(6), 20)
        self.assertEqual(self.calculator.get_price(7), 30)
        self.assertEqual(self.calculator.get_price(8), 50)
        self.assertRaises(AssertionError,lambda: self.calculator.get_price(9))
        self.assertRaises(AssertionError,lambda: self.calculator.get_price("abc"))
        self.assertRaises(AssertionError,lambda: self.calculator.get_price("wow"))

    @patch('app.calculator.requests.get')
    def test_get_cloud_cover(self, mock):
        calculator = Calculator(5000,"22/02/2020")

        mock.return_value.json.return_value = {'date': '2020-02-22', 'sunrise': '05:55:00', 'sunset': '19:03:00', 'moonrise': '04:13:00', 'moonset': '18:32:00', 'moonPhase': 'New Moon', 'moonIlluminationPct': 0, 'minTempC': 14, 'maxTempC': 25, 'avgTempC': 21, 'sunHours': 7.2, 'uvIndex': 6, 'location': {'id': 'ff1b3713-6f4e-4f53-8a61-c87e8bdeb075', 'postcode': '5000', 'name': 'ADELAIDE', 'state': 'SA', 'latitude': '-34.9328294', 'longitude': '138.6038129', 'distanceToNearestWeatherStationMetres': 1043.459920267202, 'nearestWeatherStation': {'name': 'ROBERTS STREET (UNLEY)', 'state': 'SA', 'latitude': '-34.9422', 'longitude': '138.6032'}}, 'hourlyWeatherHistory': [{'hour': 0, 'tempC': 15, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 19, 'windDirectionDeg': 131, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 73, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 1, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 18, 'windDirectionDeg': 124, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 71, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 2, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 117, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 70, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 3, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 14, 'windDirectionDeg': 110, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 68, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 4, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 109, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 67, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 5, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 107, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 67, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 6, 'tempC': 14, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 4, 'windspeedKph': 9, 'windDirectionDeg': 105, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 66, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 7, 'tempC': 16, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 8, 'windDirectionDeg': 101, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 58, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 8, 'tempC': 19, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 7, 'windDirectionDeg': 97, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 50, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 9, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 6, 'windDirectionDeg': 93, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 42, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 10, 'tempC': 22, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 7, 'windDirectionDeg': 137, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 40, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 11, 'tempC': 24, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 8, 'windDirectionDeg': 181, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 38, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 12, 'tempC': 25, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 7, 'windspeedKph': 9, 'windDirectionDeg': 225, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 36, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 13, 'tempC': 25, 'weatherDesc': 'Sunny', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 11, 'windDirectionDeg': 219, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 37, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 14, 'tempC': 24, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 12, 'windDirectionDeg': 212, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 39, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 15, 'tempC': 24, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 2, 'uvIndex': 6, 'windspeedKph': 14, 'windDirectionDeg': 206, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 40, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 16, 'tempC': 23, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 15, 'windDirectionDeg': 185, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 42, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 17, 'tempC': 22, 'weatherDesc': 'Sunny', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 16, 'windDirectionDeg': 164, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 45, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 18, 'tempC': 21, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 17, 'windDirectionDeg': 143, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 47, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 19, 'tempC': 20, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 136, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 52, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 20, 'tempC': 18, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 14, 'windDirectionDeg': 130, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 57, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 21, 'tempC': 17, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 123, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 61, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 22, 'tempC': 16, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 12, 'windDirectionDeg': 118, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 63, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 23, 'tempC': 16, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 112, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 64, 'visibilityKm': 10, 'pressureMb': 1019}]}

        # single digit month, double digit day, end_time >= start_time, non midnight start_time hour
        self.assertEqual(calculator.get_cloud_cover("22/02/2020", "17:30", "17:59"), 1)

        # single digit month, double digit day, end_time >= start_time, non midnight start_time hour
        self.assertEqual(calculator.get_cloud_cover("22/02/2020", "18:00", "18:26"), 0)

        # single digit month, double digit day, end_time >= start_time, midnight start_time hour
        self.assertEqual(calculator.get_cloud_cover("22/02/2020", "00:00", "00:59"), 0)

        mock.return_value.json.return_value = {'date': '2020-10-03', 'sunrise': '05:55:00', 'sunset': '19:03:00', 'moonrise': '04:13:00', 'moonset': '18:32:00', 'moonPhase': 'New Moon', 'moonIlluminationPct': 0, 'minTempC': 14, 'maxTempC': 25, 'avgTempC': 21, 'sunHours': 7.2, 'uvIndex': 6, 'location': {'id': 'ff1b3713-6f4e-4f53-8a61-c87e8bdeb075', 'postcode': '5000', 'name': 'ADELAIDE', 'state': 'SA', 'latitude': '-34.9328294', 'longitude': '138.6038129', 'distanceToNearestWeatherStationMetres': 1043.459920267202, 'nearestWeatherStation': {'name': 'ROBERTS STREET (UNLEY)', 'state': 'SA', 'latitude': '-34.9422', 'longitude': '138.6032'}}, 'hourlyWeatherHistory': [{'hour': 0, 'tempC': 15, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 19, 'windDirectionDeg': 131, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 73, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 1, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 18, 'windDirectionDeg': 124, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 71, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 2, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 117, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 70, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 3, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 14, 'windDirectionDeg': 110, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 68, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 4, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 109, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 67, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 5, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 107, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 67, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 6, 'tempC': 14, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 4, 'windspeedKph': 9, 'windDirectionDeg': 105, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 66, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 7, 'tempC': 16, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 8, 'windDirectionDeg': 101, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 58, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 8, 'tempC': 19, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 7, 'windDirectionDeg': 97, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 50, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 9, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 6, 'windDirectionDeg': 93, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 42, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 10, 'tempC': 22, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 7, 'windDirectionDeg': 137, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 40, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 11, 'tempC': 24, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 8, 'windDirectionDeg': 181, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 38, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 12, 'tempC': 25, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 7, 'windspeedKph': 9, 'windDirectionDeg': 225, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 36, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 13, 'tempC': 25, 'weatherDesc': 'Sunny', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 11, 'windDirectionDeg': 219, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 37, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 14, 'tempC': 24, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 12, 'windDirectionDeg': 212, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 39, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 15, 'tempC': 24, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 2, 'uvIndex': 6, 'windspeedKph': 14, 'windDirectionDeg': 206, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 40, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 16, 'tempC': 23, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 15, 'windDirectionDeg': 185, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 42, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 17, 'tempC': 22, 'weatherDesc': 'Sunny', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 16, 'windDirectionDeg': 164, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 45, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 18, 'tempC': 21, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 17, 'windDirectionDeg': 143, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 47, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 19, 'tempC': 20, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 136, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 52, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 20, 'tempC': 18, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 14, 'windDirectionDeg': 130, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 57, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 21, 'tempC': 17, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 123, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 61, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 22, 'tempC': 16, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 12, 'windDirectionDeg': 118, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 63, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 23, 'tempC': 16, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 112, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 64, 'visibilityKm': 10, 'pressureMb': 1019}]}

        # double digit month, single digit day, end_time >= start_time, midnight start_time hour
        self.assertEqual(calculator.get_cloud_cover("03/10/2020", "00:00", "00:59"), 0)

        mock.return_value.json.return_value = {'date': '2020-02-22', 'sunrise': '05:55:00', 'sunset': '19:03:00', 'moonrise': '04:13:00', 'moonset': '18:32:00', 'moonPhase': 'New Moon', 'moonIlluminationPct': 0, 'minTempC': 14, 'maxTempC': 25, 'avgTempC': 21, 'sunHours': 7.2, 'uvIndex': 6, 'location': {'id': 'ff1b3713-6f4e-4f53-8a61-c87e8bdeb075', 'postcode': '5000', 'name': 'ADELAIDE', 'state': 'SA', 'latitude': '-34.9328294', 'longitude': '138.6038129', 'distanceToNearestWeatherStationMetres': 1043.459920267202, 'nearestWeatherStation': {'name': 'ROBERTS STREET (UNLEY)', 'state': 'SA', 'latitude': '-34.9422', 'longitude': '138.6032'}}, 'hourlyWeatherHistory': [{'hour': 0, 'tempC': 15, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 19, 'windDirectionDeg': 131, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 73, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 1, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 18, 'windDirectionDeg': 124, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 71, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 2, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 117, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 70, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 3, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 14, 'windDirectionDeg': 110, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 68, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 4, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 109, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 67, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 5, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 107, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 67, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 6, 'tempC': 14, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 4, 'windspeedKph': 9, 'windDirectionDeg': 105, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 66, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 7, 'tempC': 16, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 8, 'windDirectionDeg': 101, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 58, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 8, 'tempC': 19, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 7, 'windDirectionDeg': 97, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 50, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 9, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 6, 'windDirectionDeg': 93, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 42, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 10, 'tempC': 22, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 7, 'windDirectionDeg': 137, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 40, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 11, 'tempC': 24, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 8, 'windDirectionDeg': 181, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 38, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 12, 'tempC': 25, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 7, 'windspeedKph': 9, 'windDirectionDeg': 225, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 36, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 13, 'tempC': 25, 'weatherDesc': 'Sunny', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 11, 'windDirectionDeg': 219, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 37, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 14, 'tempC': 24, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 12, 'windDirectionDeg': 212, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 39, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 15, 'tempC': 24, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 2, 'uvIndex': 6, 'windspeedKph': 14, 'windDirectionDeg': 206, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 40, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 16, 'tempC': 23, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 15, 'windDirectionDeg': 185, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 42, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 17, 'tempC': 22, 'weatherDesc': 'Sunny', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 16, 'windDirectionDeg': 164, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 45, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 18, 'tempC': 21, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 17, 'windDirectionDeg': 143, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 47, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 19, 'tempC': 20, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 136, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 52, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 20, 'tempC': 18, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 14, 'windDirectionDeg': 130, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 57, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 21, 'tempC': 17, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 123, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 61, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 22, 'tempC': 16, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 12, 'windDirectionDeg': 118, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 63, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 23, 'tempC': 16, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 112, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 64, 'visibilityKm': 10, 'pressureMb': 1019}]}

        # test cases where end_time < start_time, ValueError expected
        self.assertRaises(ValueError, lambda: calculator.get_cloud_cover("22/02/2020", "23:15", "23:05"))
        self.assertRaises(ValueError, lambda: calculator.get_cloud_cover("22/02/2020", "23:15", "21:05"))

    @patch('app.calculator.requests.get')
    def test_get_sun_hour(self, mock):
        self.calculator = Calculator(5000, "10/09/2021")

        mock.return_value.json.return_value = {'date': '2021-02-02', 'sunrise': '05:36:00', 'sunset': '19:22:00', 'moonrise': '22:22:00', 'moonset': '09:57:00', 'moonPhase': 'Waning Gibbous', 'moonIlluminationPct': 55, 'minTempC': 14, 'maxTempC': 22, 'avgTempC': 19, 'sunHours': 7.6, 'uvIndex': 5, 'location': {'id': 'ff1b3713-6f4e-4f53-8a61-c87e8bdeb075', 'postcode': '5000', 'name': 'ADELAIDE', 'state': 'SA', 'latitude': '-34.9328294', 'longitude': '138.6038129', 'distanceToNearestWeatherStationMetres': 1043.459920267202, 'nearestWeatherStation': {'name': 'ROBERTS STREET (UNLEY)', 'state': 'SA', 'latitude': '-34.9422', 'longitude': '138.6032'}}, 'hourlyWeatherHistory': [{'hour': 0, 'tempC': 14, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 46, 'uvIndex': 1, 'windspeedKph': 18, 'windDirectionDeg': 160, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 84, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 1, 'tempC': 14, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 48, 'uvIndex': 1, 'windspeedKph': 18, 'windDirectionDeg': 159, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 82, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 2, 'tempC': 14, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 51, 'uvIndex': 1, 'windspeedKph': 18, 'windDirectionDeg': 158, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 80, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 3, 'tempC': 15, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 54, 'uvIndex': 1, 'windspeedKph': 17, 'windDirectionDeg': 157, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 79, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 4, 'tempC': 15, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 58, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 156, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 78, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 5, 'tempC': 15, 'weatherDesc': 'Cloudy', 'cloudCoverPct': 63, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 155, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 77, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 6, 'tempC': 15, 'weatherDesc': 'Cloudy', 'cloudCoverPct': 67, 'uvIndex': 4, 'windspeedKph': 15, 'windDirectionDeg': 154, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 76, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 7, 'tempC': 16, 'weatherDesc': 'Cloudy', 'cloudCoverPct': 55, 'uvIndex': 4, 'windspeedKph': 15, 'windDirectionDeg': 154, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 71, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 8, 'tempC': 17, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 44, 'uvIndex': 5, 'windspeedKph': 14, 'windDirectionDeg': 155, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 65, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 9, 'tempC': 18, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 32, 'uvIndex': 5, 'windspeedKph': 14, 'windDirectionDeg': 155, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 60, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 10, 'tempC': 19, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 21, 'uvIndex': 5, 'windspeedKph': 15, 'windDirectionDeg': 160, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 54, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 11, 'tempC': 20, 'weatherDesc': 'Sunny', 'cloudCoverPct': 11, 'uvIndex': 6, 'windspeedKph': 16, 'windDirectionDeg': 165, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 48, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 12, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 18, 'windDirectionDeg': 171, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 43, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 13, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 19, 'windDirectionDeg': 170, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 41, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 14, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 20, 'windDirectionDeg': 170, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 39, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 15, 'tempC': 22, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 21, 'windDirectionDeg': 170, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 37, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 16, 'tempC': 20, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 21, 'windDirectionDeg': 166, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 45, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 17, 'tempC': 19, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 21, 'windDirectionDeg': 161, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 52, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 18, 'tempC': 17, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 22, 'windDirectionDeg': 157, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 59, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 19, 'tempC': 16, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 21, 'windDirectionDeg': 152, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 65, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 20, 'tempC': 15, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 21, 'windDirectionDeg': 147, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 71, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 21, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 20, 'windDirectionDeg': 142, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 77, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 22, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 19, 'windDirectionDeg': 137, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 78, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 23, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 18, 'windDirectionDeg': 133, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 80, 'visibilityKm': 10, 'pressureMb': 1017}]}

        self.assertEqual(self.calculator.get_sun_hour("02/02/2021"), 7.6)

        mock.return_value.json.return_value = {'date': '2020-02-22', 'sunrise': '05:55:00', 'sunset': '19:03:00', 'moonrise': '04:13:00', 'moonset': '18:32:00', 'moonPhase': 'New Moon', 'moonIlluminationPct': 0, 'minTempC': 14, 'maxTempC': 25, 'avgTempC': 21, 'sunHours': 7.2, 'uvIndex': 6, 'location': {'id': 'ff1b3713-6f4e-4f53-8a61-c87e8bdeb075', 'postcode': '5000', 'name': 'ADELAIDE', 'state': 'SA', 'latitude': '-34.9328294', 'longitude': '138.6038129', 'distanceToNearestWeatherStationMetres': 1043.459920267202, 'nearestWeatherStation': {'name': 'ROBERTS STREET (UNLEY)', 'state': 'SA', 'latitude': '-34.9422', 'longitude': '138.6032'}}, 'hourlyWeatherHistory': [{'hour': 0, 'tempC': 15, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 19, 'windDirectionDeg': 131, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 73, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 1, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 18, 'windDirectionDeg': 124, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 71, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 2, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 117, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 70, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 3, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 14, 'windDirectionDeg': 110, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 68, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 4, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 109, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 67, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 5, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 107, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 67, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 6, 'tempC': 14, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 4, 'windspeedKph': 9, 'windDirectionDeg': 105, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 66, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 7, 'tempC': 16, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 8, 'windDirectionDeg': 101, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 58, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 8, 'tempC': 19, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 7, 'windDirectionDeg': 97, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 50, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 9, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 6, 'windDirectionDeg': 93, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 42, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 10, 'tempC': 22, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 7, 'windDirectionDeg': 137, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 40, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 11, 'tempC': 24, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 8, 'windDirectionDeg': 181, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 38, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 12, 'tempC': 25, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 7, 'windspeedKph': 9, 'windDirectionDeg': 225, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 36, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 13, 'tempC': 25, 'weatherDesc': 'Sunny', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 11, 'windDirectionDeg': 219, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 37, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 14, 'tempC': 24, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 12, 'windDirectionDeg': 212, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 39, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 15, 'tempC': 24, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 2, 'uvIndex': 6, 'windspeedKph': 14, 'windDirectionDeg': 206, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 40, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 16, 'tempC': 23, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 15, 'windDirectionDeg': 185, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 42, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 17, 'tempC': 22, 'weatherDesc': 'Sunny', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 16, 'windDirectionDeg': 164, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 45, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 18, 'tempC': 21, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 17, 'windDirectionDeg': 143, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 47, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 19, 'tempC': 20, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 136, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 52, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 20, 'tempC': 18, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 14, 'windDirectionDeg': 130, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 57, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 21, 'tempC': 17, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 123, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 61, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 22, 'tempC': 16, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 12, 'windDirectionDeg': 118, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 63, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 23, 'tempC': 16, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 112, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 64, 'visibilityKm': 10, 'pressureMb': 1019}]}

        self.assertEqual(self.calculator.get_sun_hour("22/02/2020"), 7.2)

    @patch('app.calculator.requests.get')
    def test_get_day_light_length(self, mock):
        self.calculator = Calculator(5000, "02/02/2021")

        mock.return_value.json.return_value ={'date': '2021-02-02', 'sunrise': '05:36:00', 'sunset': '19:22:00', 'moonrise': '22:22:00', 'moonset': '09:57:00', 'moonPhase': 'Waning Gibbous', 'moonIlluminationPct': 55, 'minTempC': 14, 'maxTempC': 22, 'avgTempC': 19, 'sunHours': 7.6, 'uvIndex': 5, 'location': {'id': 'ff1b3713-6f4e-4f53-8a61-c87e8bdeb075', 'postcode': '5000', 'name': 'ADELAIDE', 'state': 'SA', 'latitude': '-34.9328294', 'longitude': '138.6038129', 'distanceToNearestWeatherStationMetres': 1043.459920267202, 'nearestWeatherStation': {'name': 'ROBERTS STREET (UNLEY)', 'state': 'SA', 'latitude': '-34.9422', 'longitude': '138.6032'}}, 'hourlyWeatherHistory': [{'hour': 0, 'tempC': 14, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 46, 'uvIndex': 1, 'windspeedKph': 18, 'windDirectionDeg': 160, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 84, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 1, 'tempC': 14, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 48, 'uvIndex': 1, 'windspeedKph': 18, 'windDirectionDeg': 159, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 82, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 2, 'tempC': 14, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 51, 'uvIndex': 1, 'windspeedKph': 18, 'windDirectionDeg': 158, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 80, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 3, 'tempC': 15, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 54, 'uvIndex': 1, 'windspeedKph': 17, 'windDirectionDeg': 157, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 79, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 4, 'tempC': 15, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 58, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 156, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 78, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 5, 'tempC': 15, 'weatherDesc': 'Cloudy', 'cloudCoverPct': 63, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 155, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 77, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 6, 'tempC': 15, 'weatherDesc': 'Cloudy', 'cloudCoverPct': 67, 'uvIndex': 4, 'windspeedKph': 15, 'windDirectionDeg': 154, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 76, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 7, 'tempC': 16, 'weatherDesc': 'Cloudy', 'cloudCoverPct': 55, 'uvIndex': 4, 'windspeedKph': 15, 'windDirectionDeg': 154, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 71, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 8, 'tempC': 17, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 44, 'uvIndex': 5, 'windspeedKph': 14, 'windDirectionDeg': 155, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 65, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 9, 'tempC': 18, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 32, 'uvIndex': 5, 'windspeedKph': 14, 'windDirectionDeg': 155, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 60, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 10, 'tempC': 19, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 21, 'uvIndex': 5, 'windspeedKph': 15, 'windDirectionDeg': 160, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 54, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 11, 'tempC': 20, 'weatherDesc': 'Sunny', 'cloudCoverPct': 11, 'uvIndex': 6, 'windspeedKph': 16, 'windDirectionDeg': 165, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 48, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 12, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 18, 'windDirectionDeg': 171, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 43, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 13, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 19, 'windDirectionDeg': 170, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 41, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 14, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 20, 'windDirectionDeg': 170, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 39, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 15, 'tempC': 22, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 21, 'windDirectionDeg': 170, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 37, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 16, 'tempC': 20, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 21, 'windDirectionDeg': 166, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 45, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 17, 'tempC': 19, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 21, 'windDirectionDeg': 161, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 52, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 18, 'tempC': 17, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 22, 'windDirectionDeg': 157, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 59, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 19, 'tempC': 16, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 21, 'windDirectionDeg': 152, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 65, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 20, 'tempC': 15, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 21, 'windDirectionDeg': 147, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 71, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 21, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 20, 'windDirectionDeg': 142, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 77, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 22, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 19, 'windDirectionDeg': 137, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 78, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 23, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 18, 'windDirectionDeg': 133, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 80, 'visibilityKm': 10, 'pressureMb': 1017}]}

        # sunset_minute < sunrise_minute
        self.assertAlmostEqual(self.calculator.get_day_light_length("02/02/2021"), 13.77, 2)

        mock.return_value.json.return_value ={'date': '2020-02-22', 'sunrise': '05:55:00', 'sunset': '19:03:00', 'moonrise': '04:13:00', 'moonset': '18:32:00', 'moonPhase': 'New Moon', 'moonIlluminationPct': 0, 'minTempC': 14, 'maxTempC': 25, 'avgTempC': 21, 'sunHours': 7.2, 'uvIndex': 6, 'location': {'id': 'ff1b3713-6f4e-4f53-8a61-c87e8bdeb075', 'postcode': '5000', 'name': 'ADELAIDE', 'state': 'SA', 'latitude': '-34.9328294', 'longitude': '138.6038129', 'distanceToNearestWeatherStationMetres': 1043.459920267202, 'nearestWeatherStation': {'name': 'ROBERTS STREET (UNLEY)', 'state': 'SA', 'latitude': '-34.9422', 'longitude': '138.6032'}}, 'hourlyWeatherHistory': [{'hour': 0, 'tempC': 15, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 19, 'windDirectionDeg': 131, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 73, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 1, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 18, 'windDirectionDeg': 124, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 71, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 2, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 117, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 70, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 3, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 14, 'windDirectionDeg': 110, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 68, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 4, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 109, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 67, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 5, 'tempC': 14, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 107, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 67, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 6, 'tempC': 14, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 4, 'windspeedKph': 9, 'windDirectionDeg': 105, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 66, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 7, 'tempC': 16, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 8, 'windDirectionDeg': 101, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 58, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 8, 'tempC': 19, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 7, 'windDirectionDeg': 97, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 50, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 9, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 6, 'windDirectionDeg': 93, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 42, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 10, 'tempC': 22, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 7, 'windDirectionDeg': 137, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 40, 'visibilityKm': 10, 'pressureMb': 1022}, {'hour': 11, 'tempC': 24, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 6, 'windspeedKph': 8, 'windDirectionDeg': 181, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 38, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 12, 'tempC': 25, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 7, 'windspeedKph': 9, 'windDirectionDeg': 225, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 36, 'visibilityKm': 10, 'pressureMb': 1021}, {'hour': 13, 'tempC': 25, 'weatherDesc': 'Sunny', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 11, 'windDirectionDeg': 219, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 37, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 14, 'tempC': 24, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 12, 'windDirectionDeg': 212, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 39, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 15, 'tempC': 24, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 2, 'uvIndex': 6, 'windspeedKph': 14, 'windDirectionDeg': 206, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 40, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 16, 'tempC': 23, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 15, 'windDirectionDeg': 185, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 42, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 17, 'tempC': 22, 'weatherDesc': 'Sunny', 'cloudCoverPct': 1, 'uvIndex': 6, 'windspeedKph': 16, 'windDirectionDeg': 164, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 45, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 18, 'tempC': 21, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 17, 'windDirectionDeg': 143, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 47, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 19, 'tempC': 20, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 16, 'windDirectionDeg': 136, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 52, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 20, 'tempC': 18, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 14, 'windDirectionDeg': 130, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 57, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 21, 'tempC': 17, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 123, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 61, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 22, 'tempC': 16, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 12, 'windDirectionDeg': 118, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 63, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 23, 'tempC': 16, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 112, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 64, 'visibilityKm': 10, 'pressureMb': 1019}]}

        # sunset_minute < sunrise_minute
        self.assertAlmostEqual(self.calculator.get_day_light_length("22/02/2020"), 13.13, 2)

        mock.return_value.json.return_value ={'date': '2020-12-25', 'sunrise': '05:01:00', 'sunset': '19:31:00', 'moonrise': '15:03:00', 'moonset': '01:43:00', 'moonPhase': 'Waxing Gibbous', 'moonIlluminationPct': 70, 'minTempC': 12, 'maxTempC': 25, 'avgTempC': 21, 'sunHours': 8.9, 'uvIndex': 6, 'location': {'id': 'ff1b3713-6f4e-4f53-8a61-c87e8bdeb075', 'postcode': '5000', 'name': 'ADELAIDE', 'state': 'SA', 'latitude': '-34.9328294', 'longitude': '138.6038129', 'distanceToNearestWeatherStationMetres': 1043.459920267202, 'nearestWeatherStation': {'name': 'ROBERTS STREET (UNLEY)', 'state': 'SA', 'latitude': '-34.9422', 'longitude': '138.6032'}}, 'hourlyWeatherHistory': [{'hour': 0, 'tempC': 13, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 2, 'uvIndex': 1, 'windspeedKph': 14, 'windDirectionDeg': 117, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 77, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 1, 'tempC': 13, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 19, 'uvIndex': 1, 'windspeedKph': 14, 'windDirectionDeg': 113, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 75, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 2, 'tempC': 12, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 36, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 108, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 74, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 3, 'tempC': 12, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 53, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 104, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 73, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 4, 'tempC': 12, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 39, 'uvIndex': 1, 'windspeedKph': 12, 'windDirectionDeg': 102, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 71, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 5, 'tempC': 13, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 26, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 100, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 69, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 6, 'tempC': 13, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 13, 'uvIndex': 4, 'windspeedKph': 10, 'windDirectionDeg': 98, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 68, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 7, 'tempC': 16, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 14, 'uvIndex': 5, 'windspeedKph': 8, 'windDirectionDeg': 96, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 59, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 8, 'tempC': 18, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 15, 'uvIndex': 5, 'windspeedKph': 6, 'windDirectionDeg': 95, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 50, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 9, 'tempC': 21, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 16, 'uvIndex': 6, 'windspeedKph': 4, 'windDirectionDeg': 94, 'windDirectionCompass': 'E', 'precipitationMm': 0, 'humidityPct': 41, 'visibilityKm': 10, 'pressureMb': 1020}, {'hour': 10, 'tempC': 22, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 20, 'uvIndex': 6, 'windspeedKph': 6, 'windDirectionDeg': 146, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 40, 'visibilityKm': 10, 'pressureMb': 1019}, {'hour': 11, 'tempC': 24, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 25, 'uvIndex': 6, 'windspeedKph': 8, 'windDirectionDeg': 199, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 38, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 12, 'tempC': 25, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 30, 'uvIndex': 6, 'windspeedKph': 10, 'windDirectionDeg': 252, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 36, 'visibilityKm': 10, 'pressureMb': 1018}, {'hour': 13, 'tempC': 25, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 27, 'uvIndex': 6, 'windspeedKph': 12, 'windDirectionDeg': 241, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 36, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 14, 'tempC': 25, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 24, 'uvIndex': 6, 'windspeedKph': 14, 'windDirectionDeg': 230, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 37, 'visibilityKm': 10, 'pressureMb': 1016}, {'hour': 15, 'tempC': 25, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 20, 'uvIndex': 6, 'windspeedKph': 16, 'windDirectionDeg': 219, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 37, 'visibilityKm': 10, 'pressureMb': 1016}, {'hour': 16, 'tempC': 24, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 14, 'uvIndex': 6, 'windspeedKph': 15, 'windDirectionDeg': 206, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 40, 'visibilityKm': 10, 'pressureMb': 1016}, {'hour': 17, 'tempC': 23, 'weatherDesc': 'Sunny', 'cloudCoverPct': 7, 'uvIndex': 6, 'windspeedKph': 14, 'windDirectionDeg': 193, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 43, 'visibilityKm': 10, 'pressureMb': 1016}, {'hour': 18, 'tempC': 22, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 180, 'windDirectionCompass': 'S', 'precipitationMm': 0, 'humidityPct': 46, 'visibilityKm': 10, 'pressureMb': 1016}, {'hour': 19, 'tempC': 20, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 162, 'windDirectionCompass': 'SSE', 'precipitationMm': 0, 'humidityPct': 52, 'visibilityKm': 10, 'pressureMb': 1016}, {'hour': 20, 'tempC': 19, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 143, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 57, 'visibilityKm': 10, 'pressureMb': 1016}, {'hour': 21, 'tempC': 18, 'weatherDesc': 'Clear', 'cloudCoverPct': 0, 'uvIndex': 1, 'windspeedKph': 12, 'windDirectionDeg': 125, 'windDirectionCompass': 'SE', 'precipitationMm': 0, 'humidityPct': 63, 'visibilityKm': 10, 'pressureMb': 1017}, {'hour': 22, 'tempC': 17, 'weatherDesc': 'Clear', 'cloudCoverPct': 2, 'uvIndex': 1, 'windspeedKph': 10, 'windDirectionDeg': 119, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 62, 'visibilityKm': 10, 'pressureMb': 1016}, {'hour': 23, 'tempC': 17, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 4, 'uvIndex': 1, 'windspeedKph': 8, 'windDirectionDeg': 113, 'windDirectionCompass': 'ESE', 'precipitationMm': 0, 'humidityPct': 61, 'visibilityKm': 10, 'pressureMb': 1016}]}

        # sunset_minute > sunrise_minute
        self.assertAlmostEqual(self.calculator.get_day_light_length("25/12/2020"), 14.5, 2)

    @patch('app.calculator.requests.get')
    def test_calculate_solar_energy_within_a_day_by_hour_w_cc(self, mock_1):
        self.calculator = Calculator(7250, "22/12/2022")

        self.calculator.location_id = "22d72902-b72f-4ca0-a522-4dbfb77a7b78"
        a = {'date': '2021-02-22', 'sunrise': '05:44:00', 'sunset': '19:06:00', 'moonrise': '15:43:00', 'moonset': '00:01:00', 'moonPhase': 'Waxing Gibbous', 'moonIlluminationPct': 73, 'minTempC': 9, 'maxTempC': 21, 'avgTempC': 17, 'sunHours': 5.3, 'uvIndex': 5, 'location': {'id': '22d72902-b72f-4ca0-a522-4dbfb77a7b78', 'postcode': '7250', 'name': 'BLACKSTONE HEIGHTS', 'state': 'TAS', 'latitude': '-41.46', 'longitude': '147.0820001', 'distanceToNearestWeatherStationMetres': 5607.391317385195, 'nearestWeatherStation': {'name': 'LAUNCESTON (TI TREE BEND)', 'state': 'TAS', 'latitude': '-41.4194', 'longitude': '147.1219'}}, 'hourlyWeatherHistory': [
            {'hour': 0, 'tempC': 13, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 1, 'uvIndex': 1, 'windspeedKph': 2, 'windDirectionDeg': 232, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 89, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 1, 'tempC': 12, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 3, 'uvIndex': 1, 'windspeedKph': 2, 'windDirectionDeg': 258, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 91, 'visibilityKm': 8, 'pressureMb': 1007},
            {'hour': 2, 'tempC': 11, 'weatherDesc': 'Clear', 'cloudCoverPct': 6, 'uvIndex': 1, 'windspeedKph': 3, 'windDirectionDeg': 284, 'windDirectionCompass': 'WNW', 'precipitationMm': 0, 'humidityPct': 93, 'visibilityKm': 6, 'pressureMb': 1006},
            {'hour': 3, 'tempC': 9, 'weatherDesc': 'Clear', 'cloudCoverPct': 9, 'uvIndex': 1, 'windspeedKph': 3, 'windDirectionDeg': 310, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 95, 'visibilityKm': 5, 'pressureMb': 1006},
            {'hour': 4, 'tempC': 10, 'weatherDesc': 'Clear', 'cloudCoverPct': 7, 'uvIndex': 1, 'windspeedKph': 4, 'windDirectionDeg': 314, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 93, 'visibilityKm': 6, 'pressureMb': 1006},
            {'hour': 5, 'tempC': 10, 'weatherDesc': 'Mist', 'cloudCoverPct': 6, 'uvIndex': 1, 'windspeedKph': 4, 'windDirectionDeg': 319, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 90, 'visibilityKm': 6, 'pressureMb': 1006},
            {'hour': 6, 'tempC': 10, 'weatherDesc': 'Mist', 'cloudCoverPct': 4, 'uvIndex': 3, 'windspeedKph': 4, 'windDirectionDeg': 324, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 88, 'visibilityKm': 7, 'pressureMb': 1007},
            {'hour': 7, 'tempC': 12, 'weatherDesc': 'Mist', 'cloudCoverPct': 3, 'uvIndex': 3, 'windspeedKph': 6, 'windDirectionDeg': 313, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 78, 'visibilityKm': 8, 'pressureMb': 1007},
            {'hour': 8, 'tempC': 14, 'weatherDesc': 'Sunny', 'cloudCoverPct': 1, 'uvIndex': 4, 'windspeedKph': 7, 'windDirectionDeg': 303, 'windDirectionCompass': 'WNW', 'precipitationMm': 0, 'humidityPct': 68, 'visibilityKm': 9, 'pressureMb': 1007},
            {'hour': 9, 'tempC': 16, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 8, 'windDirectionDeg': 292, 'windDirectionCompass': 'WNW', 'precipitationMm': 0, 'humidityPct': 58, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 10, 'tempC': 18, 'weatherDesc': 'Sunny', 'cloudCoverPct': 6, 'uvIndex': 5, 'windspeedKph': 10, 'windDirectionDeg': 286, 'windDirectionCompass': 'WNW', 'precipitationMm': 0, 'humidityPct': 52, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 11, 'tempC': 19, 'weatherDesc': 'Sunny', 'cloudCoverPct': 12, 'uvIndex': 5, 'windspeedKph': 11, 'windDirectionDeg': 281, 'windDirectionCompass': 'W', 'precipitationMm': 0, 'humidityPct': 45, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 12, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 17, 'uvIndex': 6, 'windspeedKph': 13, 'windDirectionDeg': 275, 'windDirectionCompass': 'W', 'precipitationMm': 0, 'humidityPct': 39, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 13, 'tempC': 20, 'weatherDesc': 'Sunny', 'cloudCoverPct': 19, 'uvIndex': 6, 'windspeedKph': 14, 'windDirectionDeg': 270, 'windDirectionCompass': 'W', 'precipitationMm': 0, 'humidityPct': 38, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 14, 'tempC': 20, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 20, 'uvIndex': 5, 'windspeedKph': 15, 'windDirectionDeg': 264, 'windDirectionCompass': 'W', 'precipitationMm': 0, 'humidityPct': 38, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 15, 'tempC': 20, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 22, 'uvIndex': 5, 'windspeedKph': 16, 'windDirectionDeg': 259, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 37, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 16, 'tempC': 18, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 20, 'uvIndex': 5, 'windspeedKph': 15, 'windDirectionDeg': 255, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 39, 'visibilityKm': 10, 'pressureMb': 1008},
            {'hour': 17, 'tempC': 17, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 18, 'uvIndex': 5, 'windspeedKph': 14, 'windDirectionDeg': 251, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 42, 'visibilityKm': 10, 'pressureMb': 1008},
            {'hour': 18, 'tempC': 16, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 16, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 247, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 44, 'visibilityKm': 10, 'pressureMb': 1009},
            {'hour': 19, 'tempC': 15, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 14, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 237, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 50, 'visibilityKm': 10, 'pressureMb': 1010},
            {'hour': 20, 'tempC': 13, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 11, 'uvIndex': 1, 'windspeedKph': 9, 'windDirectionDeg': 227, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 55, 'visibilityKm': 10, 'pressureMb': 1011},
            {'hour': 21, 'tempC': 12, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 9, 'uvIndex': 1, 'windspeedKph': 7, 'windDirectionDeg': 217, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 60, 'visibilityKm': 10, 'pressureMb': 1012},
            {'hour': 22, 'tempC': 11, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 7, 'uvIndex': 1, 'windspeedKph': 6, 'windDirectionDeg': 212, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 64, 'visibilityKm': 10, 'pressureMb': 1012},
            {'hour': 23, 'tempC': 9, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 5, 'uvIndex': 1, 'windspeedKph': 4, 'windDirectionDeg': 207, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 68, 'visibilityKm': 10, 'pressureMb': 1012}]}
        
        mock_1.return_value.json.return_value = a
        
        cc = a['hourlyWeatherHistory']
        def c_c(cc_i, hour):
            cc_val = cc[cc_i]['cloudCoverPct']
            sunset = datetime.datetime.strptime(a['sunset'], "%H:%M:%S")
            sunrise = datetime.datetime.strptime(a['sunrise'], "%H:%M:%S")
            if sunset.minute < sunrise.minute:
                sunset -= timedelta(hours=1)
                dl = (sunset.hour - sunrise.hour) + (sunset.minute + 60 - sunrise.minute) / 60
            else :
                dl = (sunset.hour - sunrise.hour) + (sunset.minute - sunrise.minute) / 60
            
            return round(a['sunHours'] * (hour / dl) * (1 - cc_val / 100) * 50 * 0.20, 11)

        # start_time between sunrise time and sunset time, end_time after sunset time
        self.assertEqual(self.calculator.calculate_solar_energy_within_a_day_by_hour_w_cc("22/02/2021", "10:00", "20:00"), [[1000, 1100, c_c(10,1)], [1100, 1200, c_c(11,1)], [1200, 1300, c_c(12,1)], [1300, 1400, c_c(13,1)], [1400, 1500, c_c(14,1)], [1500, 1600, c_c(15,1)], [1600, 1700, c_c(16,1)], [1700, 1800, c_c(17,1)], [1800, 1900, c_c(18,1)], [1900, 2000, c_c(19,0.1)], [2000, 2000, 0.0]])

        # start_time before sunrise time, end_time before sunrise time
        self.assertEqual(self.calculator.calculate_solar_energy_within_a_day_by_hour_w_cc("22/02/2021", "03:00", "05:00"), [[300, 400, c_c(3,0)], [400, 500, c_c(4,0)], [500, 500, 0.0]])

        # start_time after sunset time
        self.assertEqual(self.calculator.calculate_solar_energy_within_a_day_by_hour_w_cc("22/02/2021", "20:00", "23:00"), [[2000, 2100, c_c(20,0)], [2100, 2200, c_c(21,0)], [2200, 2300, c_c(22,0)], [2300, 2300, 0.0]])

        # start_time before sunrise time, end_time after sunset
        self.assertEqual(self.calculator.calculate_solar_energy_within_a_day_by_hour_w_cc("22/02/2021", "05:00", "20:00"), [[500, 600, c_c(5,16/60)], [600, 700, c_c(6,1)], [700, 800, c_c(7,1)], [800, 900, c_c(8,1)], [900, 1000, c_c(9,1)], [1000, 1100, c_c(10,1)], [1100, 1200, c_c(11,1)], [1200, 1300,c_c(12,1)], [1300, 1400, c_c(13,1)], [1400, 1500, c_c(14,1)], [1500, 1600, c_c(15,1)], [1600, 1700, c_c(16,1)], [1700, 1800, c_c(17,1)], [1800, 1900,c_c(18,1)], [1900, 2000, c_c(19,0.1)], [2000, 2000, 0.0]])

        # future date
        self.assertRaises(AssertionError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour_w_cc("22/02/2023", "05:00", "20:00"))

        # invalid start_date
        self.assertRaises(ValueError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour_w_cc("abc", "05:00", "20:00"))

        # invalid start_time
        self.assertRaises(ValueError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour_w_cc("22/02/2023", "abc", "20:00"))

        # invalid end_time
        self.assertRaises(ValueError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour_w_cc("22/02/2023", "05:00", "122313"))

        # incorrect format for start_time
        self.assertRaises(ValueError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour_w_cc("22/02/2021", "25:00", "10:00"))

        # end_time < start_time
        self.assertRaises(AssertionError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour_w_cc("22/02/2021", "23:00", "22:00"))

        # non-string input
        self.assertRaises(ValueError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour_w_cc("22/02/2021", "23:00", 100))
    
    @patch('app.calculator.requests.get')
    def test_calculate_solar_energy_within_a_day_by_hour(self, mock_1):
        self.calculator = Calculator(7250, "22/02/2022")

        self.calculator.location_id = "22d72902-b72f-4ca0-a522-4dbfb77a7b78"
        a = {'date': '2021-02-22', 'sunrise': '05:44:00', 'sunset': '19:06:00', 'moonrise': '15:43:00', 'moonset': '00:01:00', 'moonPhase': 'Waxing Gibbous', 'moonIlluminationPct': 73, 'minTempC': 9, 'maxTempC': 21, 'avgTempC': 17, 'sunHours': 5.3, 'uvIndex': 5, 'location': {'id': '22d72902-b72f-4ca0-a522-4dbfb77a7b78', 'postcode': '7250', 'name': 'BLACKSTONE HEIGHTS', 'state': 'TAS', 'latitude': '-41.46', 'longitude': '147.0820001', 'distanceToNearestWeatherStationMetres': 5607.391317385195, 'nearestWeatherStation': {'name': 'LAUNCESTON (TI TREE BEND)', 'state': 'TAS', 'latitude': '-41.4194', 'longitude': '147.1219'}}, 'hourlyWeatherHistory': [
            {'hour': 0, 'tempC': 13, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 1, 'uvIndex': 1, 'windspeedKph': 2, 'windDirectionDeg': 232, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 89, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 1, 'tempC': 12, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 3, 'uvIndex': 1, 'windspeedKph': 2, 'windDirectionDeg': 258, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 91, 'visibilityKm': 8, 'pressureMb': 1007},
            {'hour': 2, 'tempC': 11, 'weatherDesc': 'Clear', 'cloudCoverPct': 6, 'uvIndex': 1, 'windspeedKph': 3, 'windDirectionDeg': 284, 'windDirectionCompass': 'WNW', 'precipitationMm': 0, 'humidityPct': 93, 'visibilityKm': 6, 'pressureMb': 1006},
            {'hour': 3, 'tempC': 9, 'weatherDesc': 'Clear', 'cloudCoverPct': 9, 'uvIndex': 1, 'windspeedKph': 3, 'windDirectionDeg': 310, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 95, 'visibilityKm': 5, 'pressureMb': 1006},
            {'hour': 4, 'tempC': 10, 'weatherDesc': 'Clear', 'cloudCoverPct': 7, 'uvIndex': 1, 'windspeedKph': 4, 'windDirectionDeg': 314, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 93, 'visibilityKm': 6, 'pressureMb': 1006},
            {'hour': 5, 'tempC': 10, 'weatherDesc': 'Mist', 'cloudCoverPct': 6, 'uvIndex': 1, 'windspeedKph': 4, 'windDirectionDeg': 319, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 90, 'visibilityKm': 6, 'pressureMb': 1006},
            {'hour': 6, 'tempC': 10, 'weatherDesc': 'Mist', 'cloudCoverPct': 4, 'uvIndex': 3, 'windspeedKph': 4, 'windDirectionDeg': 324, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 88, 'visibilityKm': 7, 'pressureMb': 1007},
            {'hour': 7, 'tempC': 12, 'weatherDesc': 'Mist', 'cloudCoverPct': 3, 'uvIndex': 3, 'windspeedKph': 6, 'windDirectionDeg': 313, 'windDirectionCompass': 'NW', 'precipitationMm': 0, 'humidityPct': 78, 'visibilityKm': 8, 'pressureMb': 1007},
            {'hour': 8, 'tempC': 14, 'weatherDesc': 'Sunny', 'cloudCoverPct': 1, 'uvIndex': 4, 'windspeedKph': 7, 'windDirectionDeg': 303, 'windDirectionCompass': 'WNW', 'precipitationMm': 0, 'humidityPct': 68, 'visibilityKm': 9, 'pressureMb': 1007},
            {'hour': 9, 'tempC': 16, 'weatherDesc': 'Sunny', 'cloudCoverPct': 0, 'uvIndex': 5, 'windspeedKph': 8, 'windDirectionDeg': 292, 'windDirectionCompass': 'WNW', 'precipitationMm': 0, 'humidityPct': 58, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 10, 'tempC': 18, 'weatherDesc': 'Sunny', 'cloudCoverPct': 6, 'uvIndex': 5, 'windspeedKph': 10, 'windDirectionDeg': 286, 'windDirectionCompass': 'WNW', 'precipitationMm': 0, 'humidityPct': 52, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 11, 'tempC': 19, 'weatherDesc': 'Sunny', 'cloudCoverPct': 12, 'uvIndex': 5, 'windspeedKph': 11, 'windDirectionDeg': 281, 'windDirectionCompass': 'W', 'precipitationMm': 0, 'humidityPct': 45, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 12, 'tempC': 21, 'weatherDesc': 'Sunny', 'cloudCoverPct': 17, 'uvIndex': 6, 'windspeedKph': 13, 'windDirectionDeg': 275, 'windDirectionCompass': 'W', 'precipitationMm': 0, 'humidityPct': 39, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 13, 'tempC': 20, 'weatherDesc': 'Sunny', 'cloudCoverPct': 19, 'uvIndex': 6, 'windspeedKph': 14, 'windDirectionDeg': 270, 'windDirectionCompass': 'W', 'precipitationMm': 0, 'humidityPct': 38, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 14, 'tempC': 20, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 20, 'uvIndex': 5, 'windspeedKph': 15, 'windDirectionDeg': 264, 'windDirectionCompass': 'W', 'precipitationMm': 0, 'humidityPct': 38, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 15, 'tempC': 20, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 22, 'uvIndex': 5, 'windspeedKph': 16, 'windDirectionDeg': 259, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 37, 'visibilityKm': 10, 'pressureMb': 1007},
            {'hour': 16, 'tempC': 18, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 20, 'uvIndex': 5, 'windspeedKph': 15, 'windDirectionDeg': 255, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 39, 'visibilityKm': 10, 'pressureMb': 1008},
            {'hour': 17, 'tempC': 17, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 18, 'uvIndex': 5, 'windspeedKph': 14, 'windDirectionDeg': 251, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 42, 'visibilityKm': 10, 'pressureMb': 1008},
            {'hour': 18, 'tempC': 16, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 16, 'uvIndex': 1, 'windspeedKph': 13, 'windDirectionDeg': 247, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 44, 'visibilityKm': 10, 'pressureMb': 1009},
            {'hour': 19, 'tempC': 15, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 14, 'uvIndex': 1, 'windspeedKph': 11, 'windDirectionDeg': 237, 'windDirectionCompass': 'WSW', 'precipitationMm': 0, 'humidityPct': 50, 'visibilityKm': 10, 'pressureMb': 1010},
            {'hour': 20, 'tempC': 13, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 11, 'uvIndex': 1, 'windspeedKph': 9, 'windDirectionDeg': 227, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 55, 'visibilityKm': 10, 'pressureMb': 1011},
            {'hour': 21, 'tempC': 12, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 9, 'uvIndex': 1, 'windspeedKph': 7, 'windDirectionDeg': 217, 'windDirectionCompass': 'SW', 'precipitationMm': 0, 'humidityPct': 60, 'visibilityKm': 10, 'pressureMb': 1012},
            {'hour': 22, 'tempC': 11, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 7, 'uvIndex': 1, 'windspeedKph': 6, 'windDirectionDeg': 212, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 64, 'visibilityKm': 10, 'pressureMb': 1012},
            {'hour': 23, 'tempC': 9, 'weatherDesc': 'Partly cloudy', 'cloudCoverPct': 5, 'uvIndex': 1, 'windspeedKph': 4, 'windDirectionDeg': 207, 'windDirectionCompass': 'SSW', 'precipitationMm': 0, 'humidityPct': 68, 'visibilityKm': 10, 'pressureMb': 1012}]}
        
        mock_1.return_value.json.return_value = a

        def s_p(hour):
            sunset = datetime.datetime.strptime(a['sunset'], "%H:%M:%S")
            sunrise = datetime.datetime.strptime(a['sunrise'], "%H:%M:%S")
            if sunset.minute < sunrise.minute:
                sunset -= timedelta(hours=1)
                dl = (sunset.hour - sunrise.hour) + (sunset.minute + 60 - sunrise.minute) / 60
            else :
                dl = (sunset.hour - sunrise.hour) + (sunset.minute - sunrise.minute) / 60
            
            return round(a['sunHours'] * (hour / dl) * 50 * 0.20, 11)

        # start_time between sunrise time and sunset time, end_time after sunset time
        self.assertEqual(self.calculator.calculate_solar_energy_within_a_day_by_hour("22/02/2021", "10:00", "20:00"), [[1000, 1100, s_p(1)], [1100, 1200, s_p(1)], [1200, 1300, s_p(1)], [1300, 1400, s_p(1)], [1400, 1500, s_p(1)], [1500, 1600, s_p(1)], [1600, 1700, s_p(1)], [1700, 1800, s_p(1)], [1800, 1900, s_p(1)], [1900, 2000, s_p(0.1)], [2000, 2000, 0.0]])

        # start_time before sunrise time, end_time before sunrise time
        self.assertEqual(self.calculator.calculate_solar_energy_within_a_day_by_hour("22/02/2021", "03:00", "05:00"), [[300, 400, s_p(0)], [400, 500, s_p(0)], [500, 500, 0.0]])

        # start_time after sunset time
        self.assertEqual(self.calculator.calculate_solar_energy_within_a_day_by_hour("22/02/2021", "20:00", "23:00"), [[2000, 2100, s_p(0)], [2100, 2200, s_p(0)], [2200, 2300, s_p(0)], [2300, 2300, 0.0]])

        # start_time before sunrise time, end_time after sunset
        self.assertEqual(self.calculator.calculate_solar_energy_within_a_day_by_hour("22/02/2021", "05:00", "20:00"), [[500, 600, s_p(16/60)], [600, 700, s_p(1)], [700, 800, s_p(1)], [800, 900, s_p(1)], [900, 1000, s_p(1)], [1000, 1100, s_p(1)], [1100, 1200, s_p(1)], [1200, 1300,s_p(1)], [1300, 1400, s_p(1)], [1400, 1500, s_p(1)], [1500, 1600, s_p(1)], [1600, 1700, s_p(1)], [1700, 1800, s_p(1)], [1800, 1900,s_p(1)], [1900, 2000, s_p(0.1)], [2000, 2000, 0.0]])

        # future date
        self.assertRaises(AssertionError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour("22/02/2023", "05:00", "20:00") )

        # invalid start_date
        self.assertRaises(ValueError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour("abc", "05:00", "20:00"))

        # invalid start_time
        self.assertRaises(ValueError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour("22/02/2021", "abc", "20:00"))

        # invalid end_time
        self.assertRaises(ValueError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour("22/02/2021", "05:00", "122313"))

        # incorrect format for start_time
        self.assertRaises(ValueError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour("22/02/2021", "25:00", "10:00"))

        # end_time < start_time
        self.assertRaises(AssertionError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour("22/02/2021", "23:00", "22:00"))

        # non-string input
        self.assertRaises(ValueError, lambda: self.calculator.calculate_solar_energy_within_a_day_by_hour("22/02/2021", "23:00", 100))
    
    @patch('app.calculator.requests.get')
    def test_get_duration(self, mock):
        self.calculator = Calculator(5000, "14/09/2021")

        # test with start_time and end_time both not having hour components and end_time minute component < start_time minute
        # component
        self.assertEqual(self.calculator.get_duration("59", "1"), 2 / 60)

        # test with start_time and end_time both having single digit hour components end_time minute component >= start_time
        # minute component
        self.assertEqual(self.calculator.get_duration("125", "240"), 1.25)

        # test with start_time and end_time both having double digit hour components end_time minute component >= start_time
        # minute component
        self.assertEqual(self.calculator.get_duration("1205", "2320"), 11.25)