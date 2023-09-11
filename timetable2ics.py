import datetime

import pytz
from icalendar import Calendar, Event

from config import get_weeks_count, get_start_day, get_hours_minutes


class Course:
    name: str
    day_in_week: str
    start_at: int
    length: int
    week_array: [int]
    teacher: str
    location: str

    def __init__(self):
        self.name = ''
        self.day_in_week = ''
        self.start_at = 1
        self.length = 2
        self.week_array = ''
        self.teacher = ''
        self.location = ''

    @staticmethod
    def parse(name, day_in_week, start_at, length, week_array, teacher, location):
        course = Course()
        course.name = name
        course.day_in_week = day_in_week
        course.start_at = start_at
        course.length = length
        course.week_array = week_array
        course.teacher = teacher
        course.location = location
        return course


def generate(semester: str, course_list: [Course], append_weeks: bool) -> str:
    # 实例化cal
    cal = Calendar()
    cal.add('VERSION', '2.0')

    # 时区定义
    tz = pytz.timezone('Asia/Shanghai')

    # 获取配置定义，遍历每周的每个课程，生成ics
    weeks_count = get_weeks_count(semester)
    semester_start_day = get_start_day(semester)

    for week in range(weeks_count):  # 遍历每周
        # 添加周数标记
        if append_weeks:
            start_time = semester_start_day + datetime.timedelta(weeks=week, hours=7, minutes=30)
            end_time = semester_start_day + datetime.timedelta(weeks=week, hours=8, minutes=0)
            cal_event = Event()
            cal_event.add('summary', '第%d周' % (week + 1))
            cal_event.add('dtstart', tz.localize(start_time))
            cal_event.add('dtend', tz.localize(end_time))
            cal_event.add('description', '第%d周' % (week + 1))

            cal.add_component(cal_event)

        for course in course_list:  # 遍历每个课程
            if str(week + 1) in course.week_array:  # 如果这周有这个课程
                # 生成开始时间和结束时间
                hours, minutes = get_hours_minutes(course.start_at - 1)
                start_time = semester_start_day + datetime.timedelta(
                    weeks=week,
                    days=int(course.day_in_week) - 1,
                    hours=hours,
                    minutes=minutes)

                hours, minutes = get_hours_minutes(course.start_at + course.length - 2)
                end_time = semester_start_day + datetime.timedelta(
                    weeks=week,
                    days=int(course.day_in_week) - 1,
                    hours=hours,
                    minutes=minutes + 45)

                # 实例化cal_event
                cal_event = Event()
                cal_event.add('summary', '@'.join([course.name, course.location]))
                cal_event.add('dtstart', tz.localize(start_time))
                cal_event.add('dtend', tz.localize(end_time))
                cal_event.add('location', course.location)
                cal_event.add('description', course.teacher + '/第%d周' % (week + 1))
                # cal_event.add('key', 'value')  # 可扩展其他属性

                cal.add_component(cal_event)

    return cal.to_ical()
