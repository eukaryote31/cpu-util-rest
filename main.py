from flask import Flask
from flask_cors import CORS
import psutil
import collections
import json
import atexit
import subprocess
from flask import jsonify
from apscheduler.schedulers.background import BackgroundScheduler

LENGTH = 20
INTERVAL = 5

cpuhist = collections.deque(maxlen=LENGTH)
ramhist = collections.deque(maxlen=LENGTH)
histjson = {}
app = Flask(__name__)
CORS(app)


@app.route("/")
def cpu_pct():
    return jsonify(histjson)


def update_hist():
    cpuhist.append(psutil.cpu_percent())

    meminfo = psutil.virtual_memory()
    ramhist.append(meminfo.percent)
    numconns = int(subprocess.check_output([
        'bash', '-c', 'netstat -nap 2> /dev/null | grep 14265 | grep ESTABLISHED | wc -l'
    ]))

    global histjson
    histjson = {
        'cpu': list(cpuhist),
        'ramused': list(ramhist),
        'ramtotal': meminfo.total,
        'connections': numconns
    }


cron = BackgroundScheduler(daemon=True)
cron.add_job(update_hist, 'interval', seconds=INTERVAL)
cron.start()

atexit.register(lambda: cron.shutdown(wait=False))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=14222)
