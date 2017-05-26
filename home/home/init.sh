export FLASK_DEBUG=1
export FLASK_APP=home
pip3 install --editable .
flask initdb
flask run --host=0.0.0.0
