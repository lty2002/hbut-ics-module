from flask import Flask, request

from chengzi2ics import chengzi2ics
from config import SEMESTERS_START_DAY
from mini2ics import mini2ics

app = Flask(__name__)


@app.route('/ics/<json_type>', methods=['POST'])
def ics(json_type):
    body = request.get_json()

    semester = body.get('semester')
    timetable = body.get('data')
    if SEMESTERS_START_DAY.get(semester) is not None:
        return chengzi2ics(semester, timetable) \
            if json_type == 'chengzi' else mini2ics(semester, timetable)
    return 'Invalid semester!'


if __name__ == '__main__':
    app.run()
