import os
import time
import signal
import argparse
from parser import run_parse, stop_parse

PID_PATH = "/tmp/tut.pid"


def create_parser():
    parser = argparse.ArgumentParser(
        prog="TUT BY Parser.",
        description=(
            "Мега крутая программа для парсинга новостей\n"
            "с сайта tut.by\n"
            "Закостылил (c) Я "
        ),
        add_help=False,
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Вывести данное сообщение.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="Текущая версия.",
        version="0.1",
    )
    parser.add_argument(
        "-d",
        "--daemon",
        action="store_true",
        required=False,
        help="Запуск приложения в режиме демона.",
    )
    parser.add_argument(
        "-s",
        "--start",
        dest="start_date",
        required=False,
        help="Начальная дата.",
    )
    parser.add_argument(
        "-e",
        "--end",
        dest="end_date",
        required=False,
        help="Конечная дата.",
    )
    parser.add_argument(
        "-k",
        "--kill",
        action="store_true",
        help="Остановить приложение.",
    )
    return parser

parser = create_parser()
args = parser.parse_args()

def stop_handler(signum, frame):
    stop_parse()

def start(daemon):
    arguments = {"start_date": args.start_date}
    if args.end_date is not None:
        arguments.update(end_date=args.end_date)
    if daemon:
        if os.path.isfile(PID_PATH):
            print("Сервер уже работает!")
            return
        pid = os.fork()
        if not pid:
            with open(PID_PATH, "w") as pid_file:
                pid_file.write(str(os.getpid()))
            signal.signal(signal.SIGTERM, stop_handler)
            try:
                run_parse(**arguments)
            except Exception:
                pass
            finally:
                try:
                    os.remove(PID_PATH)
                except Exception:
                    pass
        else:
            print("Программа запущена в фоновом режиме.")
            return
    else:
        try:
            run_parse(**arguments)
        except KeyboardInterrupt:
            stop_parse()

def stop(daemon):
    if daemon:
        with open(PID_PATH, "r") as pid_file:
            pid = int(pid_file.read().strip())
        os.kill(pid, signal.SIGTERM)
        while os.path.isfile(PID_PATH):
            time.sleep(1)

if args.kill:
    try:
        stop(os.path.isfile(PID_PATH))
    except Exception:
        print("Клиент остался жив!")
else:
    start(args.daemon)