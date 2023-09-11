import logging

import pandas as pd
from flask import abort

import timetable2ics


def mini2ics(semester: str, timetable: list, append_weeks: bool = False) -> str:
    if not {'kname', 'timeWeek', 'kweekStr', 'teacherName', 'skLoc', 'timeJc'}.issubset(set(timetable[0].keys())):
        abort(400, 'Invalid timetable')
    df = pd.DataFrame(timetable)
    logging.info(df.to_json(orient='records'))
    # 以time、week、weeksArray、teacher、place为分组依据，统计每个课程的开始时间和持续节数
    event_df = df.groupby(['kname', 'timeWeek', 'kweekStr', 'teacherName', 'skLoc']).agg(
        start_at=('timeJc', lambda x: int(x.iloc[0])),
        count=('timeJc', 'count')
    ).reset_index().sort_values(['timeWeek', 'start_at'])
    event_dict = event_df.to_dict(orient='records')

    # 转为标准化的timetable
    # 注：kweekStr为逗号分隔字符串，转为列表
    standard_timetable = list(map(lambda event: {
        'week_array': event['kweekStr'].split(','),
        'name': event['kname'],
        'day_in_week': event['timeWeek'],
        'start_at': event['start_at'],
        'length': event['count'],
        'teacher': event['teacherName'],
        'location': event['skLoc']
    }, event_dict))
    course_list = list(map(lambda x: timetable2ics.Course.parse(**x), standard_timetable))

    return timetable2ics.generate(semester, course_list, append_weeks)
