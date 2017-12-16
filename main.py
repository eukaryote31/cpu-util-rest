from flask import Flask
import psutil
import collections
import json
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

LENGTH = 20
INTERVAL = 5

hist = collections.deque(maxlen=LENGTH)
app = Flask(__name__)


@app.route("/")
def cpu_pct():
    return json.dumps(list(hist))


def update_hist():
    hist.append(psutil.cpu_percent())

cron = BackgroundScheduler(daemon=True)
cron.add_job(update_hist, 'interval', seconds=INTERVAL)
cron.start()

atexit.register(lambda: cron.shutdown(wait=False))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=14222)
