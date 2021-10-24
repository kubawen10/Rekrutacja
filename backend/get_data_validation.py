from flask_restful import abort
import time_functions

def abort_if_wrong_date_format(date):
    #check if date is in "date time" format
    if time_functions.is_date_time_format(date):
        return True
    else:
        if time_functions.is_date_format(date):
            return False
        abort(400, description="Invalid date format...")