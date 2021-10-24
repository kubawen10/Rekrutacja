from flask_restful import abort
import re
import time_functions
import table_functions

def abort_if_number_of_seats_not_in_boundry(numberOfSeats, seatNumber):
    boundries = table_functions.get_seat_boundries(seatNumber)
    if boundries is None:
        abort(404, description="Invalid seat number...")
    if numberOfSeats<boundries["minNumberOfSeats"]:
        abort(409, description="Number of seats is too low for this table...")
    if numberOfSeats>boundries["maxNumberOfSeats"]:
        abort(409, description="Number of seats is too high for this table...")
        
def abort_if_wrong_date(date, duration):
    ##dd.mm.yyyy HH:MM
    dtformat=time_functions.is_date_time_format(date)
    
    if not dtformat:
        abort(409, description="Invalid date format...")
    
    if time_functions.is_in_past(dtformat):
        abort(409, description="It is not possible to place reservation in the past...")
        
    if time_functions.restaurant_is_closed(dtformat, duration):
        abort(409, description="Restaurant is closed at this time...")

def abort_if_wrong_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, email):
        abort(409, description="Invalid email...")

def abort_if_invalid_data(args):
    abort_if_number_of_seats_not_in_boundry(args.numberOfSeats, args.seatNumber)
    abort_if_wrong_date(args.date, args.duration)
    abort_if_wrong_email(args.email)
      
      
      
def abort_if_unavailable(args, reservations):
    for reservation in reservations:
        if args.seatNumber == reservation.seatNumber and time_functions.reservations_collide(args.date, args.duration, reservation.date, reservation.duration):
            abort(409, description="This seat is taken at this time...")
        
        
        
        
    
