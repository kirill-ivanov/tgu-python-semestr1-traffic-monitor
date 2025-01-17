import math
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.orm import sessionmaker

from db.init import Alert, Stat, engine

Session = sessionmaker(bind=engine)
session = Session()


def add_stat_all(type_obj_list):
    for key in type_obj_list:
        add_stat(key, type_obj_list[key])


def add_alert(type, message):
    new_alert = Alert(type=type, message=message, dt=datetime.now())
    try:
        session.add(new_alert)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"При создании уведомления возникла ошибка: {e}")


def add_stat(type, count):
    print(f"{type} added {count}")
    new_stat = Stat(type=type, count=count, dt=datetime.now())
    try:
        session.add(new_stat)

        if count > 15:
            add_alert("WARNING", f"Образовался затор ({count})")
        elif count > 18:
            add_alert("ERROR", f"Образовался пробка ({count})")

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"При создании замера возникла ошибка: {e}")


def filter_alert(type, date_from_str, date_to_str):
    sess = session.query(Alert).order_by(Alert.dt.desc())
    if type:
        sess = sess.filter(Alert.type == type)
    if date_from_str:
        date_from = datetime.strptime(date_from_str + " 00:00:00", '%d.%m.%Y %H:%M:%S')
        sess = sess.filter(Alert.dt >= date_from)
    if date_to_str:
        date_to = datetime.strptime(date_to_str + " 23:59:59", '%d.%m.%Y %H:%M:%S')
        sess = sess.filter(Alert.dt <= date_to)
    alerts = sess.all()
    return alerts


def filter_stat(type, date_from_str, date_to_str):
    sess = session.query(Stat).order_by(Stat.dt.desc())
    if type:
        sess = sess.filter(Stat.type == type)
    if date_from_str:
        date_from = datetime.strptime(date_from_str + " 00:00:00", '%d.%m.%Y %H:%M:%S')
        sess = sess.filter(Stat.dt >= date_from)
    if date_to_str:
        date_to = datetime.strptime(date_to_str + " 23:59:59", '%d.%m.%Y %H:%M:%S')
        sess = sess.filter(Stat.dt <= date_to)
    stats = sess.all()
    return stats


def last_stat():
    return session.query(Stat).order_by(Stat.dt.desc()).first()


def group_stat(type, group, date_from_str, date_to_str) -> list:
    sess = None
    if group == "hour":
        sess = (session
                .query(Stat.type,
                       func.strftime("%Y-%m-%d %H", Stat.dt).label("dt"),
                       func.avg(Stat.count).label("avg_count"))
                .group_by(Stat.type, func.strftime("%Y-%m-%d %H", Stat.dt))
                .order_by(func.strftime("%Y-%m-%d %H", Stat.dt).desc()))
    else:
        sess = (session
                .query(Stat.type,
                       func.strftime("%Y-%m-%d", Stat.dt).label("dt"),
                       func.avg(Stat.count).label("avg_count"))
                .group_by(Stat.type,
                          func.strftime("%Y-%m-%d", Stat.dt))
                .order_by(func.strftime("%Y-%m-%d %H", Stat.dt).desc()))

    if type:
        sess = sess.filter(Stat.type == type)
    if date_from_str:
        date_from = datetime.strptime(date_from_str + " 00:00:00", '%d.%m.%Y %H:%M:%S')
        sess = sess.filter(Stat.dt >= date_from)
    if date_to_str:
        date_to = datetime.strptime(date_to_str + " 23:59:59", '%d.%m.%Y %H:%M:%S')
        sess = sess.filter(Stat.dt <= date_to)

    stats = sess.all()
    result = []
    for stat in stats:
        result.append(Stat(type=stat.type, count=round(stat.avg_count), dt=stat.dt))
    return result
