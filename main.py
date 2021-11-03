from flask import Flask, flash
from flask import render_template
from flask import request
from app.calculator import *

from app.calculator_form import *
import os
SECRET_KEY = os.urandom(32)

ev_calculator_app = Flask(__name__)
ev_calculator_app.config['SECRET_KEY'] = SECRET_KEY


@ev_calculator_app.route('/', methods=['GET', 'POST'])
def operation_result():
    # request.form looks for:
    # html tags with matching "name="

    calculator_form = Calculator_Form(request.form)

    # validation of the form
    if request.method == "POST" and calculator_form.validate():

        # extract information from the form
        battery_capacity = request.form['BatteryPackCapacity']
        initial_charge = request.form['InitialCharge']
        final_charge = request.form['FinalCharge']
        start_date = request.form['StartDate']
        start_time = request.form['StartTime']
        post_code = request.form["PostCode"]
        charger_configuration = request.form['ChargerConfiguration']
        location_name = request.form['LocationName']

        lst = start_date.split('/')
        if len(lst[0]) == 1:
            day = '0' + lst[0]
        else:
            day = lst[0]
        if len(lst[1]) == 1:
            month = '0' + lst[1]
        else:
            month = lst[1]
        year = lst[2]

        start_date = day + '/' + month + '/' + year

        # if valid, create calculator to calculate the time and cost
        calculator = Calculator(post_code,start_date,location_name)

        cost1 = calculator.cost_calculation_v1(initial_charge, final_charge, battery_capacity,
                                               calculator.get_price(charger_configuration),
                                               calculator.get_power(charger_configuration),
                                               start_date, start_time)

        cost2 = calculator.cost_calculation_v2(initial_charge, final_charge, battery_capacity,
                                               calculator.get_price(charger_configuration),
                                               calculator.get_power(charger_configuration),
                                               start_date, start_time)
        cost3 = calculator.cost_calculation_v3(initial_charge, final_charge, battery_capacity,
                                               calculator.get_price(charger_configuration),
                                               calculator.get_power(charger_configuration),
                                               start_date, start_time)

        time = calculator.time_calculation(initial_charge, final_charge, battery_capacity,
                                           calculator.get_power(charger_configuration))

        # format outputs
        if time < 1:
            time = str(int(time*60)) + " minute(s)"
        else:
            arr = str(time).split('.')
            hour = arr[0]
            minute = int(int(arr[1])/100*60)
            time = str(hour) + " hour(s) " + str(minute) + " minute(s)"

        if cost1 == '-':
            cost1 = "Future date input, please refer to cost3"
        else:
            cost1 = "$" + str(round(cost1, 2))

        if cost2 == '-':
            cost2 = "Future date input, please refer to cost3"
        else:
            cost2 = "$" + str(round(cost2, 2))

        cost3 = "$" + str(round(cost3, 2))

        # you may change the return statement also
        
        # values of variables can be sent to the template for rendering the webpage that users will see
        return render_template('calculator.html', time = time, cost1=cost1, cost2=cost2, cost3=cost3,
                               calculation_success = True, form = calculator_form)
        # return render_template('calculator.html', calculation_success=True, form=calculator_form)

    else:
        # battery_capacity = request.form['BatteryPackCapacity']
        # flash(battery_capacity)
        # flash("something went wrong")
        flash_errors(calculator_form)
        return render_template('calculator.html', calculation_success = False, form = calculator_form)

# method to display all errors
def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


if __name__ == '__main__':
    ev_calculator_app.run()
