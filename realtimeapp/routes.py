from flask import Blueprint, render_template, session
from .models import Sensor

charts_page = Blueprint('charts_page', __name__,
                        template_folder='templates')

# fallback to the default sensor "sensor"
@charts_page.route('/', defaults={'sensor_name': 'sensor'})
@charts_page.route('/chart/', defaults={'sensor_name': 'sensor'})
@charts_page.route('/chart/<string:sensor_name>')
def charts(sensor_name):
    session['sensor_name']=sensor_name
    return render_template('index.html',sensor_name=sensor_name, sensors=list(Sensor.objects))
