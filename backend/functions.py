from random import randint

def reservation_dict(reservation):
    return {"id": reservation.id,
            "date": reservation.date, 
            "duration": reservation.duration, 
            "seatNumber":reservation.seatNumber, 
            "fullName":reservation.fullName, 
            "phone":reservation.phone, 
            "email":reservation.email, 
            "numberOfSeats":reservation.numberOfSeats}
    
def generateKey():
    return randint(100000,999999)
