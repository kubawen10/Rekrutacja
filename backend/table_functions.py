import json
import time_functions

def get_seat_boundries(seat_number):
    with open("seats.json") as f:
        seats_data = json.load(f)["tables"]
    for i in seats_data:
        if i["number"]==seat_number:
            i.pop("number")
            return i
    return None

def get_seats_from_list(list):
    with open("seats.json") as f:
        seats_data = json.load(f)["tables"]
    output=[]
    for seat in seats_data:
        if seat["number"] in list:
            output.append(seat)
    return output 

def get_taken_seats_number(reservations, args):
    taken=[]
    for reservation in reservations:
            if time_functions.reservations_collide(args.start_date, int(args.duration), reservation.date, reservation.duration):
                seatBoundries=get_seat_boundries(reservation.seatNumber)
                if args.min_seats>=seatBoundries["minNumberOfSeats"] and args.min_seats<=seatBoundries["maxNumberOfSeats"]:
                    taken.append(reservation.seatNumber)    
    return list(set(taken))


def get_seats_for_x_people(x):
    with open("seats.json") as f:
        seats_data = json.load(f)["tables"]
    output=[]
    for seat in seats_data:
        if seat["minNumberOfSeats"]<=x and seat["maxNumberOfSeats"]>=x:
            output.append(seat["number"])
    return output
            
        
    
    
    
    
