import requests, json

from main import Reservation

BASE = "http://127.0.0.1:5000/"

#print(Reservation.query.all())

# response = requests.post(BASE + "/reservations", {"date":"26.10.2021 20:00",
#                                                     "duration": 40,
#                                                     "seatNumber": 1,
#                                                     "fullName": "Chyba dziala",
#                                                     "phone": "123332131",
#                                                     "email": "kox@toRobil.com",
#                                                     "numberOfSeats": 6})
# print(response.json())

#reservations get test
# response = requests.get(BASE + "/reservations", {"date": "24.10.2021"})
# print(response.json())

##reservations/id put test
# response = requests.put(BASE + "/reservations/2", {"status": "requested cancelation"})
# print(response)
# # input()

##reservations/id delete test
# response = requests.delete(BASE + "/reservations/2", json={"varificationCode": "581156"})
# print(response.json())

##tables get test

# response=requests.get(BASE+"/tables", {"status": "free", "min_seats": 6, "start_date": "26.10.2021 20:00", "duration": "40"})
# print(response.json())




