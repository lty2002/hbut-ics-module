import logging
import os

from flask import Flask, request

from chengzi2ics import chengzi2ics
from mini2ics import mini2ics

app = Flask(__name__)

current_dir = os.path.abspath(__file__).rsplit("/", 1)[0]
log_path = os.path.join(current_dir, "ics-log.log")
logging.basicConfig(filename=log_path,
                    level=logging.INFO,
                    filemode='a',
                    format='[%(levelname)s]:%(asctime)s:\n%(message)s',
                    datefmt='%Y-%d-%m %H:%M:%S')


@app.route('/ics/<json_type>', methods=['POST'])
def ics(json_type):
    body = request.get_json()

    semester = body.get('semester', '2024-2024-1')
    timetable = body.get('data')
    append_weeks = body.get('appendWeeks', False)
    return mini2ics(semester, timetable, append_weeks) \
        if json_type == 'mini' else chengzi2ics(semester, timetable, append_weeks)


if __name__ == '__main__':
    app.run()
