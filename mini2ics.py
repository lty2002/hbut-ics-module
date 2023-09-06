import pandas as pd
from icalendar import Calendar, Event

from config import *


def mini2ics(semester: str, timetable: list) -> str:
    df = pd.DataFrame(timetable)
    # 以time、week、weeksArray、teacher、place为分组依据，统计每个课程的开始时间和持续节数
    event_df = df.groupby(['kname', 'timeWeek', 'kweekStr', 'teacherName', 'skLoc']).agg(
        start_at=('timeJc', lambda x: int(x.iloc[0])),
        count=('timeJc', 'count')
    ).reset_index().sort_values(['timeWeek', 'start_at'])
    event_dict = event_df.to_dict(orient='records')

    # 实例化cal
    cal = Calendar()
    cal.add('VERSION', '2.0')

    # 获取配置定义，遍历每周的每个课程，生成ics
    weeks_count = get_weeks_count(semester)
    semester_start_day = SEMESTERS_START_DAY[semester]

    for week in range(weeks_count):  # 遍历每周
        for event in event_dict:  # 遍历每个课程
            if str(week + 1) in event['kweekStr'].split(','):  # 如果这周有这个课程
                # 生成开始时间和结束时间
                hours, minutes = get_hours_minutes(event['start_at'] - 1)
                start_time = semester_start_day + datetime.timedelta(
                    weeks=week,
                    days=int(event['timeWeek']) - 1,
                    hours=hours,
                    minutes=minutes)

                hours, minutes = get_hours_minutes(event['start_at'] + event['count'] - 2)
                end_time = semester_start_day + datetime.timedelta(
                    weeks=week,
                    days=int(event['timeWeek']) - 1,
                    hours=hours,
                    minutes=minutes + 45)

                # 实例化cal_event
                cal_event = Event()
                cal_event.add('summary', '@'.join([event['kname'], event['skLoc']]))
                cal_event.add('dtstart', start_time)
                cal_event.add('dtend', end_time)
                cal_event.add('location', event['skLoc'])
                cal_event.add('description', event['teacherName'])
                # cal_event.add('key', 'value')  # 可扩展其他属性

                cal.add_component(cal_event)

    return cal.to_ical()
