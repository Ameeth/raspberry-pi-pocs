import os
import sqlite3, json
from home import app
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify, make_response
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from home import gpio, tvchannel, remote
import logging
from logging.handlers import RotatingFileHandler

nav = Nav()

Bootstrap(app)

app.config.from_object(__name__) # load config from this file

RECENT_CHANNELS = []

# Load default config and override config from an environment variable
app.config.from_envvar('HOME_AUTOMATION_CONFIG')
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'home.db')
))

logHandler = logging.FileHandler('/var/log/home_automation.log')
logHandler.setLevel(logging.INFO)
app.logger.addHandler(logHandler)
app.logger.setLevel(logging.INFO)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def dynamic_navbar():
    navbar = Navbar('Home')
    app.logger.info("Session " + str(session.get('logged_in')))
    if  session.get('logged_in'):
        navbar.items = [View('TV', 'channel_list')]
        navbar.items.append(View('LED', 'led_demo'))
        navbar.items.append(View('Logout', 'logout'))
    else :
        navbar.items.append(View('Login', 'login'))
    return navbar

nav.register_element('homenav', dynamic_navbar)

nav.init_app(app)

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('channel_list'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/channel_list')
def channel_list():
    db = get_db()
    cur = db.execute('select channel_name, channel_no, genre from tv_channel order by genre desc')
    entries = cur.fetchall()
    return render_template('tv_channels.html', entries=entries)

@app.route('/channel_json')
def channel_json():
    db = get_db()
    cur = db.execute('select channel_name, channel_no, genre from tv_channel order by genre desc')
    entries = cur.fetchall()
    listoflist = []
    for entry in entries:
        lista = tvchannel.TvChannel(entry[0], entry[1], entry[2])
        listoflist.append(lista)
    return json.dumps(listoflist,cls=tvchannel.MyEncoder)

@app.route('/recent_channel_json')
def recent_channel_json():
    db = get_db()
    placeholder= '?' # For SQLite. See DBAPI paramstyle.
    placeholders= ', '.join(placeholder for unused in RECENT_CHANNELS)
    query= 'select channel_name, channel_no, genre from tv_channel where channel_no in (%s)'  % placeholders
    cur = db.execute(query, RECENT_CHANNELS)
    entries = cur.fetchall()
    listoflist = []
    for entry in entries:
        lista = tvchannel.TvChannel(entry[0], entry[1], entry[2])
        listoflist.append(lista)
    return json.dumps(listoflist,cls=tvchannel.MyEncoder)

@app.route('/led-demo')
def led_demo():
    return render_template('led_demo.html')


@app.route('/led-glow/<color>')
def led_glow(color):
    gpio.glow_led(color)
    return jsonify( {"color":color})


@app.route('/led-switchoff')
def led_switchoff():
    gpio.glow_switchoff()
    return jsonify( {"sucess":True})

@app.route('/switch-channel/<channelno>')
def switch_channel(channelno):
    app.logger.info("Channel Switch Called " + channelno)
    remote.goto_channel(channelno)
    if(len(RECENT_CHANNELS) >= 5):
        RECENT_CHANNELS.pop()

    RECENT_CHANNELS.insert(0, channelno)
    return jsonify( {"channelno":channelno})

@app.route('/tv_mute')
def tv_mute():
    remote.mute_ts()
    return jsonify( {"sucess":True})

@app.route('/tv_onoff')
def tv_onoff():
    remote.onoff()
    return jsonify( {"sucess":True})

@app.route('/tv_volumeup')
def tv_volumeup():
    remote.volume_up_ts()
    return jsonify( {"sucess":True})

@app.route('/tv_volumedown')
def tv_volumedown():
    remote.volume_down_ts()
    return jsonify( {"sucess":True})

@app.route('/tv_channel_next')
def tv_channel_next():
    remote.channel_up()
    return jsonify( {"sucess":True})

@app.route('/tv_channel_previous')
def tv_channel_previous():
    remote.channel_down()
    return jsonify( {"sucess":True})

@app.route('/tv_go_back')
def tv_go_back():
    remote.go_back()
    return jsonify( {"sucess":True})

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    app.logger.info("Request:")
    app.logger.info(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    if req.get("result").get("action") != "switch-on-tv":
        return {}
    res = makeWebhookResult(tv_onoff())
    return res

def makeWebhookResult(data):
    # print(json.dumps(item, indent=4))

    speech = "Switching on the tv"

    app.logger.info("Response:")
    app.logger.info(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-home-automation-sample"
}
