from flask import Flask
from flask_cors import CORS
import psutil
import collections
import json
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

LENGTH = 20
INTERVAL = 5

hist = collections.deque(maxlen=LENGTH)
histjson = "[]"
app = Flask(__name__)
CORS(app)


@app.route("/")
def cpu_pct():
    return histjson


def update_hist():
    hist.append(psutil.cpu_percent())
    global histjson
    histjson = json.dumps(list(hist))


cron = BackgroundScheduler(daemon=True)
cron.add_job(update_hist, 'interval', seconds=INTERVAL)
cron.start()

atexit.register(lambda: cron.shutdown(wait=False))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=14222)
