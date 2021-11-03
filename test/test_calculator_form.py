import main
import unittest

class ObjWithData:
    """
    An object that contains an attribute 'data'. An ObjWithData instance acts as a substitute to
    the input of a Flask form. The value of the input which is accessed via input.data, allows something
    similar for ObjWithData via ObjWithData.data
    """
    def __init__(self, data):
        self.data = data

class TestCalculatorForm(unittest.TestCase):
    """
    Test class for calculator_form validation methods and helper functions.
    NOTE: Since the Flask form's inputs are all strings (it's a web app), each validate methods will
    be passed in an ObjWithData instance with "data" of type string. The actual type of "data" of concern
    is the type after converting them from string, eg for "2", the actual value we want is 2.
    """
    def setUp(self):
        main.ev_calculator_app.config["WTF_CSRF_ENABLED"] = False  # disable CSRF to prevent context errors
        with main.ev_calculator_app.app_context():
            self.calculator_form = main.Calculator_Form()
            self.calculator_form.FinalCharge.data = "80"
            self.calculator_form.InitialCharge.data = "20"

    def test_validate_battery_pack_capacity(self):
        # pass in a non-numeric character
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_BatteryPackCapacity(self.calculator_form, ObjWithData("a")))
        
        # pass in a number less than 0.65
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_BatteryPackCapacity(self.calculator_form, ObjWithData("0.01")))
        
        # pass in a number greater than 100
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_BatteryPackCapacity(self.calculator_form, ObjWithData("101")))
        
        # pass in a valid number
        self.assertEqual(None,
                         main.Calculator_Form.
                         validate_BatteryPackCapacity(self.calculator_form, ObjWithData("2")))

    def test_validate_initial_charge(self):
        # pass in a non-numeric character
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_InitialCharge(self.calculator_form, ObjWithData("!")))
        
        # pass in a number less than 0
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_InitialCharge(self.calculator_form, ObjWithData("-1")))
        
        # pass in a number greater than 100
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_InitialCharge(self.calculator_form, ObjWithData("201.4")))
        
        # pass in a number greater than FinalCharge (which is 80 as declared in setUp)
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_InitialCharge(self.calculator_form, ObjWithData("80.1")))
        
        # pass in a valid number
        self.assertEqual(None,
                         main.Calculator_Form.
                         validate_InitialCharge(self.calculator_form, ObjWithData("26")))

    def test_validate_final_charge(self):
        # pass in a non-numeric character
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_FinalCharge(self.calculator_form, ObjWithData("p")))
        
        # pass in a number less than 0
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_FinalCharge(self.calculator_form, ObjWithData("-2")))
        
        # pass in a number greater than 100
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_FinalCharge(self.calculator_form, ObjWithData("11111")))
        
        # pass in a number lesser than Initial Charge (which is 20 as declared in setUp)
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_FinalCharge(self.calculator_form, ObjWithData("12")))
        
        # pass in a valid number
        self.assertEqual(None,
                         main.Calculator_Form.
                         validate_FinalCharge(self.calculator_form, ObjWithData("26")))

    def test_validate_start_date(self):
        # pass in an invalid date (earlier than 1st July 2008)
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_StartDate(self.calculator_form, ObjWithData("1999-02-02")))
        
        # pass in a valid date (later than 1st July 2008)
        self.assertEqual(None,
                         main.Calculator_Form.
                         validate_StartDate(self.calculator_form, ObjWithData("2008-07-02")))

    def test_validate_charger_configuration(self):
        # pass in a non-integer character
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_ChargerConfiguration(self.calculator_form, ObjWithData("2.2")))
        
        # pass in a number lesser than 1
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_ChargerConfiguration(self.calculator_form, ObjWithData("0")))
        
        # pass in a number greater than 8
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_ChargerConfiguration(self.calculator_form, ObjWithData("9")))
        
        # pass in a valid number
        self.assertEqual(None,
                         main.Calculator_Form.
                         validate_ChargerConfiguration(self.calculator_form, ObjWithData("1")))

    def test_validate_postcode(self):
        # pass in a non-integer character
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_PostCode(self.calculator_form, ObjWithData("abc")))
        
        # pass in a number lesser than 200
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_PostCode(self.calculator_form, ObjWithData("199")))
        
        # pass in a number greater than 9729
        self.assertRaises(ValueError,
                          lambda: main.Calculator_Form.
                          validate_PostCode(self.calculator_form, ObjWithData("9999")))
        
        # pass in a valid number
        self.assertEqual(None,
                         main.Calculator_Form.
                         validate_PostCode(self.calculator_form, ObjWithData("4000")))

    def test_isfloat(self):
        # pass in a float value
        self.assertTrue(main.isfloat("2.4"))
        
        # pass in a non-float value, but convertible to float
        self.assertTrue(main.isfloat("1"))
        
        # pass in a non-float value, and inconvertible to float
        self.assertFalse(main.isfloat("abc"))