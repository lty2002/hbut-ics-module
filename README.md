# ics-module

## Description
本项目可以由`橙子课表`/`Mini湖工`友好的数据生成ics文件，用于导入日历

## Dependencies
- python3
- pip3
- pandas
- icalendar
- flask(optional)
- gunicorn(optional)

## Deployment
```shell
cd /path/to/project
python3 -m pip install -r requirements.in
python3 app.py                                    # dev env
python3 -m gunicorn -c gunicorn_config.py app:app # prod env
```