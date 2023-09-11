import json
import logging

import pandas as pd
from flask import abort

import timetable2ics


def chengzi2ics(semester: str, timetable: list, append_weeks: bool = False) -> str:
    if not {'name', 'time', 'week', 'weeksArray', 'teacher', 'place'}.issubset(set(timetable[0].keys())):
        abort(400, 'Invalid timetable')
    df = pd.DataFrame(timetable)
    logging.info(df.to_json(orient='records'))
    # 以time、week、weeksArray、teacher、place为分组依据，统计每个课程的开始时间和持续节数
    event_df = df.groupby(['name', 'week', 'weeksArray', 'teacher', 'place']).agg(
        start_at=('time', lambda x: int(x.iloc[0][-2:])),
        count=('time', 'count')
    ).reset_index().sort_values(['week', 'start_at'])
    event_dict = event_df.to_dict(orient='records')

    # 转为标准化的timetable
    # 注：weeksArray为json字符串，反序列化，转为列表
    standard_timetable = list(map(lambda event: {
        'week_array': json.loads(event['weeksArray']),
        'name': event['name'],
        'day_in_week': event['week'],
        'start_at': event['start_at'],
        'length': event['count'],
        'teacher': event['teacher'],
        'location': event['place']
    }, event_dict))
    course_list = list(map(lambda x: timetable2ics.Course.parse(**x), standard_timetable))

    return timetable2ics.generate(semester, course_list, append_weeks)
