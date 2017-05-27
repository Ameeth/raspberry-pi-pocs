export FLASK_DEBUG=0
export FLASK_APP=home
export HOME_AUTOMATION_CONFIG=/home/pi/home_automation/raspberry-pi-pocs/settings.cfg
pip3 install --editable .
flask initdb
flask run --host=0.0.0.0
