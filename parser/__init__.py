from .tut import TutBy
from datetime import date, timedelta

WORK = True


def run_parse(start_date: str, end_date: str = None):
    start = date.strptime(start_date, "%d.%m.%Y")
    if end_date is not None:
        end = date.strptime(end_date, "%d.%m.%Y")
    else:
        end = date.today()
    delta_days = 0
    while WORK:
        curent_date = start + timedelta(days=delta_days)
        tut_by = TutBy(curent_date.strftime("%d.%m.%Y"))
        tut_by.parse_bs()
        for news in tut_by:
            # запишем в базу
            pass
        if curent_date = end:
            WORK = False
        else:
            delta_days += 1
    else:
        pass


def stop_parse():
    WORK = False