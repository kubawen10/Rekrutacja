from datetime import datetime, timedelta
import re

dateTimeFormat= "%d.%m.%Y %H:%M"
dateFormat="%d.%m.%Y"

def is_date_time_format(date):
    try:
        dtformat=datetime.strptime(date, dateTimeFormat)
        return dtformat
    except ValueError:
        return False

def is_date_format(date):
    try:
        dFormat=datetime.strptime(date, dateFormat)
        return dFormat
    except ValueError:
        return False
    
def is_in_past(date):
    now=datetime.now()
    now=now.strftime(dateTimeFormat)    
    now=datetime.strptime(now, dateTimeFormat)
    return date<now

def restaurant_is_closed(date,duration):
    #asume restaurant is open from 10 to 21
    openHour=10
    closeHour=21
    
    open=date.replace(hour=openHour, minute=0)
    close=date.replace(hour=closeHour, minute=0)
    resDuration=date+timedelta(minutes=duration)
    return date<open or date>close or resDuration>close

def reservations_collide(date1, duration1, date2, duration2):
    b1=datetime.strptime(date1, dateTimeFormat)
    e1=b1+timedelta(minutes=duration1)
    b2=datetime.strptime(date2, dateTimeFormat)
    e2=b2+timedelta(minutes=duration2)
    if (b1<=b2 and b2<=e1) or (b2<=b1 and b1<=e2):
        return True
    return False

def is_after(date1, date2):
    dt=is_date_time_format(date1)
    resdt=is_date_time_format(date2)
    if dt.date()==resdt.date() and dt.time()<=resdt.time():
        return True
    return False

def less_than_two_hours(date):
    reservationTime=is_date_time_format(date)
    return reservationTime-datetime.now() < timedelta(hours=2)


    

    