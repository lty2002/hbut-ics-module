import datetime

SEMESTERS_START_DAY = {
    '2020-2021-1': datetime.datetime(2020, 9, 7, 0, 0, 0),
    '2020-2021-2': datetime.datetime(2021, 3, 1, 0, 0, 0),
    '2021-2022-1': datetime.datetime(2021, 9, 6, 0, 0, 0),
    '2021-2022-2': datetime.datetime(2022, 2, 21, 0, 0, 0),
    '2022-2023-1': datetime.datetime(2022, 8, 29, 0, 0, 0),
    '2022-2023-2': datetime.datetime(2023, 2, 13, 0, 0, 0),
    '2023-2024-1': datetime.datetime(2023, 9, 4, 0, 0, 0),
    '2023-2024-2': datetime.datetime(2024, 2, 26, 0, 0, 0),
    '2024-2025-1': datetime.datetime(2024, 9, 2, 0, 0, 0),
    '2024-2025-2': datetime.datetime(2025, 2, 24, 0, 0, 0),
    '2025-2026-1': datetime.datetime(2025, 9, 1, 0, 0, 0),
    '2025-2026-2': datetime.datetime(2026, 2, 23, 0, 0, 0)
}

DEFAULT_WEEKS_COUNT = 18


def get_weeks_count(semester):
    return DEFAULT_WEEKS_COUNT if semester.endswith('1') else 19


CLASS_START_TIME = ['08:20', '09:10', '10:15', '11:05',
                    '14:00', '14:50', '15:55', '16:45',
                    '18:30', '19:20', '20:10']


def get_hours_minutes(index):
    return map(int, CLASS_START_TIME[index].split(':'))
